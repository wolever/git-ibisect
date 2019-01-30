``git-ibisect``: interactively run git bisect (with undo!)
==========================================================

**ALPHA WARNING**: this project is still *very alpha*!

``git-ibisect`` is an interactive wrapper around ``git bisect`` which makes it
easy to run bisect from any directory (not just the repository root), run a
series of commands before each step, and undo mistakes made while bisecting:

<pre><code>$ <strong>git ibisect</strong>
guess which commit is first good commit (hash, branch, or a number of commits back): <strong>5</strong>
git bisect start
git bisect bad
git checkout HEAD~5
&gt; Note: checking out 'HEAD~5'.
&gt;
&gt; You are in 'detached HEAD' state. You can look around, make experimental
&gt; changes and commit them, and you can discard any commits you make in this
&gt; state without impacting any branches by performing another checkout.
&gt;
&gt; If you want to create a new branch to retain commits you create, you may
&gt; do so (now or later) by using -b with the checkout command again. Example:
&gt;
&gt;   git checkout -b &lt;new-branch-name&gt;
&gt;
&gt; HEAD is now at 40bafc4 Initial

hint: test this commit to see if it is good or bad:
 ibisect&gt; run make clean && make && make test

ibisect (no good)&gt; <strong>run exit 0</strong> <em>(simulate a passing test)</em>
'exit 0' exited with status 0
mark this commit as good [Y/n]: <strong>y</strong>
git bisect good
&gt; Bisecting: 2 revisions left to test after this (roughly 1 step)
&gt; [d2934c797d4412319e04f12944899eff6fb9975a] Add license, installation
re-run 'exit 0' [Y/n]: <strong>y</strong>

'exit 0' exited with status 0
mark this commit as good [Y/n]: <strong>y</strong>
git bisect good
&gt; Bisecting: 0 revisions left to test after this (roughly 1 step)
&gt; [65acd6c743160df3188a030ae0445c38d453baf7] Add status command
re-run 'exit 0' [Y/n]: <strong>n</strong>
ibisect (~1 commits)&gt;
ibisect (~1 commits)&gt; <strong>run exit 1</strong> <em>(simulate a failing test)</em>
'exit 1' exited with status 256
mark this commit as bad [Y/n]: <strong>y</strong>
git bisect bad
&gt; Bisecting: 0 revisions left to test after this (roughly 0 steps)
&gt; [40541a4876058652e102852e8b891077412cce74] Fix undo
re-run 'exit 1' [Y/n]: <strong>y</strong>

'exit 1' exited with status 256
mark this commit as bad [Y/n]: <strong>y</strong>
git bisect bad
&gt; 40541a4876058652e102852e8b891077412cce74 is the first bad commit
&gt; commit 40541a4876058652e102852e8b891077412cce74
&gt; Author: David Wolever &lt;david@wolever.net&gt;
&gt; Date:   Tue Jan 29 17:36:58 2019 -0500
&gt;
&gt;     Fix undo
&gt;
&gt; :100755 100755 8712b09... c00918d... M	git-ibisect
ibisect (finished: 40541a48)&gt; <strong>status</strong>
finished; first bad commit:
 commit 40541a4876058652e102852e8b891077412cce74
 Author: David Wolever &lt;david@wolever.net&gt;

     Fix undo

bisect start: master
log:
 git bisect start
 # bad: [9ab80228293442815f697c744794cfd8b2ac71d5] Way user friendly stuff
 git bisect bad 9ab80228293442815f697c744794cfd8b2ac71d5
 # good: [40bafc4b58251af39f3ee3522b96ff96598ceece] Initial
 git bisect good 40bafc4b58251af39f3ee3522b96ff96598ceece
 # good: [d2934c797d4412319e04f12944899eff6fb9975a] Add license, installation
 git bisect good d2934c797d4412319e04f12944899eff6fb9975a
 # bad: [65acd6c743160df3188a030ae0445c38d453baf7] Add status command
 git bisect bad 65acd6c743160df3188a030ae0445c38d453baf7
 # bad: [40541a4876058652e102852e8b891077412cce74] Fix undo
 git bisect bad 40541a4876058652e102852e8b891077412cce74
 # first bad commit: [40541a4876058652e102852e8b891077412cce74] Fix undo

ibisect (finished: 40541a48)&gt;</code></pre>

Installation
============

Manually:

    $ curl https://raw.githubusercontent.com/wolever/git-ibisect/master/git-ibisect -O /usr/local/bin/git-ibisect
    $ chmod +x /usr/local/bin/git-ibisect
