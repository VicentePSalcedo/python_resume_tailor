{
  description = "Python Template";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = {
    nixpkgs,
    flake-utils,
    ...
  }:
    flake-utils.lib.eachDefaultSystem (
      system: let
        pkgs = nixpkgs.legacyPackages.${system};

        python = pkgs.python312;
        pippkgs = pkgs.python312Packages;

        nativeBuildInputs = with pkgs; [
          pippkgs.beautifulsoup4
          pippkgs.cloudscraper
          pippkgs.google-generativeai
          pippkgs.requests
          python
          pyright
        ];

        buildInputs = with pkgs; [];
      in {
        devShells.default = pkgs.mkShell {inherit nativeBuildInputs buildInputs;};

        packages.default = python.pkgs.buildPythonApplication {
          pname = "template";
          version = "0.0.0";
          format = "setuptools";

          src = ./.;

          # True if tests
          doCheck = false;

          inherit nativeBuildInputs buildInputs;
        };
      }
    );
}
