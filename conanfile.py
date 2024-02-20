from conans import ConanFile, tools
from conan.tools.cmake import CMakeToolchain, CMake, CMakeDeps

class HppfclConan(ConanFile):
    name = "hpp-fcl"
    version = "2.1.2"
    settings = "cppstd", "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    # generators = "CMakeToolchain"
    requires=["eigen/3.4.0", "boost/1.78.0"]

    # all of the exports we would need to use this as a conan-package.
    exports_sources = ["**/**", "CMakeLists.txt"]

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def generate(self):
        tc = self._configure_cmake()
        tc.generate()

        deps = CMakeDeps(self)
        deps.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["hpp-fcl"]

    def _configure_cmake(self):
        cmake = CMakeToolchain(self)
        cmake.cache_variables["BUILD_PYTHON_INTERFACE"]=False
        cmake.cache_variables["HPP_FCL_HAS_QHULL"]=False
        cmake.cache_variables["INSTALL_DOCUMENTATION"]=False

        # flags I have added:
        cmake.cache_variables["HPP_FCL_USE_OCTOMAP"]=False
        cmake.cache_variables["HPP_FCL_BUILD_SHARED_LIBRARY"]=False
        cmake.cache_variables["HPP_FCL_BUILD_CORE_ONLY"]=True

        return cmake