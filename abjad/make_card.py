import abjad
from pdf2image import convert_from_path
from PIL import Image
import glob
import os

preamble = r"""#(set-global-staff-size 19.5)

\paper {
    #(set-paper-size "a4" 'portrait)
    top-margin = 40
    left-margin = 0
    right-margin = 0
    top-system-spacing.basic-distance = #20
}

\layout {
    indent = #0
    \context {
        \Score
        \override Clef.stencil = ##f
        \override SystemStartBar.stencil = ##f
        \override TimeSignature.transparent = ##t
        proportionalNotationDuration = #(ly:make-moment 1 16)
        \override SpacingSpanner.uniform-stretching = ##t
    }
}"""


def blank_space():
    blank = abjad.Note("B4", (1, 4))
    abjad.override(blank).NoteHead.transparent = "##t"
    abjad.override(blank).Stem.stencil = "##f"
    return blank


def make_triplets(notes):
    if len(notes) % 3 != 0:
        print(f"{notes} cannot be divided by 3!")
        exit(-1)
    triplets = []
    for _ in range(int(len(notes) / 3)):
        triplet = []
        for h in range(3):
            triplet.append(notes.pop(0))
        triplets.append(abjad.Tuplet((2, 3), triplet))
    return triplets


def slur_all(notes):
    abjad.attach(abjad.StartSlur(), notes[0])
    abjad.attach(abjad.StopSlur(), notes[-1])
    return notes


def attach_staccato(note):
    stac = abjad.Articulation("staccato")
    abjad.attach(stac, note)
    return note


class CardBuilder:
    def card_0():
        notes = [abjad.Rest('r2')]
        return notes

    def card_1():
        notes = [abjad.Note("B4", (1, 4)), abjad.Note("E6", (1, 4))]
        abjad.override(notes[1]).NoteHead.style = "#'triangle"
        abjad.attach(abjad.Glissando(), notes[0])
        return slur_all(notes)

    def card_2():
        # this card needs to be spaced more!
        trill = []
        for _ in range(3):
            trill.extend([abjad.Note("B4", (1, 32)), abjad.Note("C5", (1, 32))])
        notes = slur_all(trill) + [abjad.Rest('r16')] + [blank_space()]
        return notes

    def card_3():
        notes = [abjad.Note("C5", (1, 8)), abjad.Rest('r16'), abjad.Note("G4", (1, 8)), abjad.Rest('r16'), blank_space()]
        return notes

    def card_4():
        # beaming still needs to be fixed
        div = (1, 8)
        trip = [abjad.Note(n, div) for n in ("G4", "Ab4", "G4")]
        notes = [abjad.Tuplet((2, 3), trip)]
        notes += [abjad.Note('F#4', (1, 8)), abjad.Rest('r8')]
        return notes

    def card_5():
        notes = []
        for _ in range(3):
            low_f = abjad.Note("F3", (1, 16))
            abjad.override(low_f).NoteHead.style = "#'triangle"
            notes.append(low_f)
        notes.append(abjad.Rest('r16'))
        notes.append((blank_space()))
        return notes

    def card_6():
        notes = slur_all([abjad.Note(pitch, (1, 32)) for pitch in ['G4', 'A4', 'B4', 'C5']])
        notes.append(abjad.Rest('r16'))
        notes.append((blank_space()))
        return notes

    def card_7():
        note = abjad.Note('E6', (1, 2))
        abjad.override(note).NoteHead.style = "#'triangle"
        return [note]

    def card_8():
        notes = [abjad.Note(pitch, (1, 8)) for pitch in ['A4', 'C5', 'E5', 'C5']]
        return notes

    def card_9():
        notes = [abjad.Note(pitch, (1, 8)) for pitch in ['E5', 'A4', 'C5', 'A4']]
        return notes

    def card_10():
        seven_e = [abjad.Note('E4', (1, 16)) for _ in range(7)]
        notes = [abjad.Tuplet((4, 7), seven_e)]
        notes.append(abjad.Rest('r4'))
        return notes

    def card_11():
        notes = [abjad.Note("E4", (1, 4)), abjad.Note("F5", (1, 4))]
        abjad.attach(abjad.Glissando(), notes[0])
        return slur_all(notes)

    def card_12():
        notes = [attach_staccato(abjad.Note("C5", (1, 8))) for _ in range(2)]
        notes.append(blank_space())
        return notes

    def card_13():
        notes = [abjad.Note("F5", (3, 16)) for _ in range(2)]
        notes.append(blank_space())
        grace = abjad.BeforeGraceContainer([abjad.Note("E4", (1, 8))], command=r"\acciaccatura")
        abjad.attach(grace, notes[0])
        return notes

    def card_14():
        notes = [abjad.Note(pitch, (1, 4)) for pitch in ("E4", "C5", "A4")]
        notes = make_triplets(notes)
        return notes

    def card_15():
        notes = [abjad.Note(pitch, (1, 4)) for pitch in ("C5", "E4", "A4")]
        notes = make_triplets(notes)
        return notes

    def card_16():
        notes = [abjad.Note(pitch, (1, 8)) for pitch in ("F5", "F5", "E4")]
        notes = make_triplets(notes)
        notes += [abjad.Rest((1, 8)), blank_space()]
        return notes

    def card_17():
        notes = [abjad.Note(pitch, (1, 16)) for pitch in ("D5", "G5", "C5", "G5")]
        notes += [abjad.Note("B4", (1, 8)), blank_space()]
        return notes

    def card_18():
        notes = [abjad.Note(pitch, (1, 16)) for pitch in ("B4", "G5", "C5", "G5")]
        notes += [abjad.Note("D5", (1, 8)), blank_space()]
        return notes


card_funcs = [func() for func in filter(lambda x: callable(x), CardBuilder.__dict__.values())]

i = 0

for card_base in card_funcs:
    if os.path.exists(f'../resources/card_{i}.jpg'):
        print(f"Skipping card {i}")
        i += 1
        continue
    score = abjad.Score(name="Score")
    notes = card_base + [abjad.Rest('r2') for _ in range(3)] + [abjad.Note("C5", (1, 4)) for _ in range(4)]
    container = abjad.Container(notes)
    repeat = abjad.Repeat()
    abjad.attach(repeat, container)
    staff = abjad.Staff([container])
    score.append(staff)
    note = abjad.select(score).note(0)
    time_signature = abjad.TimeSignature((12, 4))
    abjad.attach(time_signature, note)

    lilypond_file = abjad.LilyPondFile(items=[preamble, score])
    abjad.show(lilypond_file)

    all_pdfs = glob.glob(r"C:\Users\bkier\projects\draw(0)\abjad\output_dir\*.pdf")

    path = r"C:\Users\bkier\OneDrive\Desktop\poppler-21.03.0\Library\bin"

    for pdf in all_pdfs:
        pdf_images = convert_from_path(pdf, poppler_path=path)

        for pdf_image in pdf_images:
            pdf_image.save(r"output_dir\staff.jpg", "JPEG")

        jpeg_im = Image.open(r"C:\Users\bkier\projects\draw(0)\abjad\output_dir\staff.jpg")

        width, height = jpeg_im.size
        im_crop = jpeg_im.crop((50, 475, 310, 700))
        im_crop.save(f'../resources/card_{i}.jpg', quality=95)

    delete_files = glob.glob(r"C:/Users/bkier/projects/draw(0)/abjad/output_dir/*")
    for f in delete_files:
        os.remove(f)
    print(f"Built card {i}")
    i += 1
