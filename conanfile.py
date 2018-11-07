from conans import ConanFile, CMake, tools, AutoToolsBuildEnvironment
import os


class SoundtouchConan(ConanFile):
    name = "soundtouch"
    version = "1.9.2"
    description = "SoundTouch is an open-source audio processing library for changing the Tempo, Pitch and Playback Rates of audio streams or audio files"
    url = "https://github.com/conan-multimedia/soundtouch"
    homepage = 'http://www.surina.net/soundtouch/'
    license = "LGPLv2_1Plus"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "cmake"
    source_subfolder = "source_subfolder"

    def source(self):
        #tools.get('http://www.surina.net/soundtouch/{name}-{version}.tar.gz'.format(name=self.name,version=self.version))
        tools.get('http://172.16.64.65:8081/artifactory/gstreamer/{name}-{version}.tar.gz'.format(name=self.name,version=self.version))
        extracted_dir = self.name
        os.rename(extracted_dir, self.source_subfolder)

    def build(self):
        with tools.chdir(self.source_subfolder):
            self.run("./bootstrap")

            _args = ["--prefix=%s/builddir"%(os.getcwd())]
            if self.options.shared:
                _args.extend(['--enable-shared=yes','--enable-static=no'])
            else:
                _args.extend(['--enable-shared=no','--enable-static=yes'])
            autotools = AutoToolsBuildEnvironment(self)
            autotools.configure(args=_args)
            autotools.make(args=["-j4"])
            autotools.install()

    def package(self):
        if tools.os_info.is_linux:
            with tools.chdir(self.source_subfolder):
                self.copy("*", src="%s/builddir"%(os.getcwd()))

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

