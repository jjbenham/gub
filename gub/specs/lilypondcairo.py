from gub.specs import lilypond

# FIXME: this is a version of lilypond which uses pangocairo used by
# Denemo We probably do not want to build pango + cairo for standalone
# lilypond packages, because that would also pull libX11 dependencies
# in.  Hmm.

class Lilypondcairo (lilypond.Lilypond):
    source = 'http://download.linuxaudio.org/lilypond/sources/v2.18/lilypond-2.18.0.tar.gz'
    dependencies = [x.replace ('pango', 'pangocairo')
                    for x in lilypond.Lilypond.dependencies]
    def get_conflict_dict (self):
        return {'': ['lilypond']}

class Lilypondcairo__mingw (lilypond.Lilypond__mingw):
    source = Lilypondcairo.source
    dependencies = [x.replace ('pango', 'pangocairo')
                for x in lilypond.Lilypond__mingw.dependencies]
    patches = [
		'lilypond-chord-names.patch',
#        '0003-Start-OTF-font-from-E800-avoids-hardcoded-linux-unic.patch',
        ]
    def get_conflict_dict (self):
        return {'': ['lilypond']}

class Lilypondcairo__darwin (lilypond.Lilypond__darwin):
    source = Lilypondcairo.source
    dependencies = [x.replace ('pango', 'pangocairo')
                for x in lilypond.Lilypond__darwin
                .dependencies]
    def get_conflict_dict (self):
        return {'': ['lilypond']}

class Lilypondcairo__darwin__ppc (lilypond.Lilypond__darwin__ppc):
    source = Lilypondcairo.source
    dependencies = [x.replace ('pango', 'pangocairo')
                for x in lilypond.Lilypond__darwin__ppc
                .dependencies]
    def get_conflict_dict (self):
        return {'': ['lilypond']}
