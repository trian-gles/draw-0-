import abjad
from pdf2image import convert_from_path, convert_from_bytes
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)
from PIL import Image

preamble = r"""#(set-global-staff-size 35)

\paper {
    #(set-paper-size "a4" 'landscape)
    top-margin = 40
    left-margin = 0
    right-margin = 0
}

\layout {
    indent = #0

    \context {
        \Staff
        \override VerticalAxisGroup.staff-staff-spacing.minimum-distance = 16
    }
    \context {
        \Score
        \override Clef.stencil = ##f
        \override NoteHead.transparent = ##t
        \override SpacingSpanner.strict-spacing = ##t
        \override SystemStartBar.stencil = ##f
        \override Stem.stencil = ##f
        \override TimeSignature.transparent = ##t
        proportionalNotationDuration = #(ly:make-moment 1 16)
    }
}"""

score = abjad.Score(name="Score")
notes = [abjad.Rest('r2') for _ in range(4)] + [abjad.Note("C5", (1, 4)) for _ in range(4)]
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

path = r"C:\Users\bkier\OneDrive\Desktop\poppler-21.03.0\Library\bin"

pdf_images = convert_from_path(r"C:\Users\bkier\projects\draw(0)\abjad\output_dir\base_stave.pdf", poppler_path = path)

for pdf_image in pdf_images:
    pdf_image.save(r"output_dir\staff.jpg", "JPEG")

jpeg_im = Image.open(r"C:\Users\bkier\projects\draw(0)\abjad\output_dir\staff.jpg")

width, height = jpeg_im.size

print(width, height)
im_crop = jpeg_im.crop((190, 0, 600, height))
im_crop.save(r'../resources/test_card.jpg', quality=95)
