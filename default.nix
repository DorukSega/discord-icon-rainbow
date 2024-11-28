{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  name = "discord-logo-changer";

  buildInputs = [
    pkgs.python311
    pkgs.python311Packages.discordpy
    pkgs.python311Packages.pillow
  ];

}
