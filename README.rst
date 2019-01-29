``git-ibisect``: interactively run git bisect (with undo!)
==========================================================

**ALPHA WARNING**: this project is still *very alpha*!

``git-ibisect`` is an interactive wrapper around ``git bisect`` which makes it
easy to run bisect from any directory (not just the repository root), run a
series of commands before each step, and undo mistakes made while bisecting::

   myproject/src $ git ibisect
   which commit should we start with (hash, branch name, or a number of commits back): 25
   starting bisect at commit e0fc61aa1 (25 commits ago)
   git bisect start
   git bisect bad
   git checkout e0fc61aa1
   ibisect (no good)> run tox
   ...
   'tox' exited with status 0
   mark this commit as good [Y/n]: y
   git bisect good
   > Bisecting: 30 revisions left to test after this (roughly 5 steps)
   > [9f75ebf4bc86662b7611a29ec8ded42fd7ef3d2f] Fix widget bug
   re-run 'tox' [Y/n]: y
   ...
   'tox' exited with status 1
   mark this commit as bad [Y/n]: y
   git bisect bad
   > Bisecting: 17 revisions left to test after this (roughly 4 steps)
   > [7a5bab8d348f2ea837fb3495e9a20e6963cabb41] Make the button red
   re-run 'tox' [Y/n]: n
   ibisect (~17 commits)> undo
   undoing 'git bisect bad' at revision 9f75ebf4
   ibisect (~30 commits)> good
   git bisect good
   > Bisecting: 16 revisions left to test after this (roughly 4 steps)
   > [dce6716418415ec17adc60d01196a285e4ecf6b5] Add --foo option
