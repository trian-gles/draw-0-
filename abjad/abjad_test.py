import abjad

preamble = r"""#(set-global-staff-size 45)

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
notes = [abjad.Note("C5", (1, 4)) for _ in range(12)]
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
