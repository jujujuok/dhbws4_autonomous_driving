let
  pkgs = import (fetchTarball "https://github.com/NixOS/nixpkgs/archive/9a9960b98418f8c385f52de3b09a63f9c561427a.tar.gz") {};
  python = 
    let packageOverrides = self: super: {
      opencv4 = super.opencv4.override {
        enableGtk2 = true;
	gtk2 = pkgs.gtk2;
      };
    };
    in pkgs.python310.override {inherit packageOverrides; self = python;};  
in pkgs.mkShell {
  packages = [
    (python.withPackages (py-pkg: [
       py-pkg.pillow
       py-pkg.pygame
       py-pkg.numpy
       py-pkg.matplotlib
       py-pkg.scipy
       py-pkg.opencv4
       py-pkg.gymnasium
       py-pkg.pybox2d
    ]))
  ];
}
