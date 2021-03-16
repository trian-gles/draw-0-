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
        \override SpacingSpanner.strict-spacing = ##t
        \override SystemStartBar.stencil = ##f
        \override TimeSignature.transparent = ##t
        proportionalNotationDuration = #(ly:make-moment 1 16)
    }
}"""


def slur_all(notes):
    abjad.attach(abjad.StartSlur(), notes[0])
    abjad.attach(abjad.StopSlur(), notes[-1])
    return notes


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
        trill . extend([abjad.Note("B4", (1, 32)), abjad.Note("C5", (1, 32))])
    notes = slur_all(trill) + [abjad.Rest('r16')]
    return notes


card_funcs = (card_0, card_1, card_2)

i = 0

for func in card_funcs:
    score = abjad.Score(name="Score")
    notes = func() + [abjad.Rest('r2') for _ in range(3)] + [abjad.Note("C5", (1, 4)) for _ in range(4)]
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
        im_crop = jpeg_im.crop((10, 475, 270, 700))
        im_crop.save(f'../resources/card_{i}.jpg', quality=95)

    delete_files = glob.glob(r"C:/Users/bkier/projects/draw(0)/abjad/output_dir/*")
    for f in delete_files:
        os.remove(f)
    print(f"Built card {i}")
    i += 1
