global = { \key c \major }sopMusic = \absolute { d'' }altoMusic = \absolute { d' }tenorMusic = \absolute { b }bassMusic = \absolute { g, }\score { \new ChoirStaff <<\new Staff = "women" << \new Voice = "sopranos" { \voiceOne << \global \sopMusic >> }\new Voice = "altos" { \voiceTwo << \global \altoMusic >> } >>\new Staff = "men" << \clef bass \new Voice = "tenors" { \voiceOne << \global \tenorMusic >> }\new Voice = "basses" { \voiceTwo << \global \bassMusic >> } >> >> } \version "2.18.2"