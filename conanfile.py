from conans import ConanFile, tools, AutoToolsBuildEnvironment, MSBuild
from conanos.build import config_scheme
import os, shutil


class SoundtouchConan(ConanFile):
    name = "soundtouch"
    version = "2.1.2"
    description = "SoundTouch is an open-source audio processing library for changing the Tempo, Pitch and Playback Rates of audio streams or audio files"
    url = "https://github.com/conanos/soundtouch"
    homepage = 'http://www.surina.net/soundtouch/'
    license = "LGPL-2.1+"
    exports = ["COPYING.TXT", "SoundTouchDLL.rc"]
    generators = "visual_studio", "gcc"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = { 'shared': True, 'fPIC': True }

    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        del self.settings.compiler.libcxx

        config_scheme(self)

    def source(self):
        url_ = 'https://gitlab.com/soundtouch/soundtouch/-/archive/{version}/soundtouch-{version}.tar.gz'
        tools.get(url_.format(version=self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)
        if self.settings.os == 'Windows':
            shutil.copy2(os.path.join(self.source_folder,"SoundTouchDLL.rc"),
                         os.path.join(self.source_folder,self._source_subfolder,"source","SoundTouchDLL","SoundTouchDLL.rc"))

    def build(self):
        #with tools.chdir(self.source_subfolder):
        #    self.run("./bootstrap")

        #    _args = ["--prefix=%s/builddir"%(os.getcwd())]
        #    if self.options.shared:
        #        _args.extend(['--enable-shared=yes','--enable-static=no'])
        #    else:
        #        _args.extend(['--enable-shared=no','--enable-static=yes'])
        #    autotools = AutoToolsBuildEnvironment(self)
        #    autotools.configure(args=_args)
        #    autotools.make(args=["-j4"])
        #    autotools.install()

        if self.settings.os == 'Windows':
            with tools.chdir(os.path.join(self._source_subfolder,"source")):
                msbuild = MSBuild(self)
                msbuild.build("SoundTouch\SoundTouch.sln",upgrade_project=True,platforms={'x86': 'Win32', 'x86_64': 'x64'})
                msbuild.build("SoundTouchDLL\SoundTouchDLL.sln",upgrade_project=True,platforms={'x86': 'Win32', 'x86_64': 'x64'})
                msbuild.build("SoundStretch\soundstretch.vcxproj",upgrade_project=True,platforms={'x86': 'Win32', 'x86_64': 'x64'})

    def package(self):
        if self.settings.os == 'Windows':
            self.copy("*.exe", dst=os.path.join(self.package_folder,"bin"), src=os.path.join(self.build_folder,self._source_subfolder,"bin"))
            self.copy("SoundTouch.h", dst=os.path.join(self.package_folder,"include"), src=os.path.join(self.build_folder,self._source_subfolder,"include"))
            if self.options.shared:
                self.copy("SoundTouchDLL*.lib", dst=os.path.join(self.package_folder,"lib"), src=os.path.join(self.build_folder,self._source_subfolder,"lib"))
                self.copy("SoundTouchDLL*.dll", dst=os.path.join(self.package_folder,"lib"), src=os.path.join(self.build_folder,self._source_subfolder,"bin"))
            else:
                self.copy("SoundTouch*.lib", dst=os.path.join(self.package_folder,"lib"), src=os.path.join(self.build_folder,self._source_subfolder,"lib"), excludes="SoundTouchDLL*.lib")


    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

