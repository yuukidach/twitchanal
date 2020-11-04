# Software Guide

## Getting Started

Since all the group members ( except me :joy:) are using MacBook. These steps can help you set up a workstation.

1. Install [Homebrew](https://www.howtogeek.com/211541/homebrew-for-os-x-easily-installs-desktop-apps-and-terminal-utilities/).
2. Install [iTerm2](https://www.iterm2.com/) (recommended).
3. Install Fish and [Oh My Fish](https://theworkaround.com/2016/10/11/installing-fish-on-osx.html) (recommended).
      `brew install fish`
4. Install python3.
      `brew install python3`
5. Install pip (should be installed with python3 if you used Homebrew, use `pip3 --version` to check).
6. Install Git
      `brew install git`
7. Install Git LFS
      `brew install git-lfs`
8. [Create ssh key and upload public key to github](https://www.testingexcellence.com/install-git-mac-generate-ssh-keys/)

## Coding Style

We are using Python and we can follow the [coding style of Google](https://google.github.io/styleguide/pyguide.html).


## Git(Hub)

If you have time, you can read the [Pro Git](https://git-scm.com/book/en/v2) book. But I know we all have many other works to do. So I just write some topics about Git that we will encounter in the our project.

### Key points

1. Create a new branch from master branch when you are working. (DO NOT commit to master branch directly)
2. Don't have multiple long-term maintained branches.
3. Don't commit to other teammates' branches.
4. After your work is finished, created a PR (pull request) to master and add a reviewer to review your code.
5. Use `git lfs` to track large files and certain binary files.

### GitHub workflow

This is a team project, we want to have a simple and clean history of our work. We need to [understand the GitHub flow](https://guides.github.com/introduction/flow/).

### Basic usage of git

https://rogerdudler.github.io/git-guide/

The most simple way is to remember whenever you make changes to you work, you use the commands

``` git
git add .
git commit -m "<your comment for you commit>"
git push origin <your branch>
```

Replace the contents in `< >` based on your situation.
