`git-ibisect`: interactively run git bisect (with undo!)
========================================================

**ALPHA WARNING**: this project is still *very alpha*!

`git-ibisect` is an interactive wrapper around `git bisect` which makes it
easy to run bisect from any directory (not just the repository root), run a
series of commands before each step, and undo mistakes made while bisecting.

What is `git bisect`?
---------------------

Problem: a thing is broken. It worked last week but doesn't work this week,
and it's not obvious why.

`git bisect` helps you figure out why.

Specifically, if you know that something is working in one commit but broken
in another, `git bisect` will help you [binary search](https://www.khanacademy.org/computing/computer-science/algorithms/binary-search/a/binary-search)
between the working - "good" - commit and the broken - "bad" - commit to find
the commit which introduced the breaking change.

Bisecting with `git ibisect` by Example
---------------------------------------

Consider a common problem: after doing a clean install, you notice that
something is broken and tests are failing. The tests work on your colleague's
machine, though, so you suspect it's a dependency-related issue, but you're not
sure when the broken dependency was introduced.

First, you confirm that the tests are failing on a clean install:

<pre><code>$ <strong>rm -r node_modules/</strong>
$ <strong>npm install</strong>
...
$ <strong>npm run test</strong>
...
Tests failed!</code></pre>

Next, you'll start `ibisect`, which will prompt you to guess which commit was
working:

<pre><code>$ git <strong>ibisect</strong>
guess which commit is first good commit (hash, branch, or a number of commits back):</code></pre>

You can enter a commit hash or branch name, but it's often simplest to guess a
number of commits. You think things were working `50` commits ago, so you enter
`50`. This will start the bisect process (`git bisect start`), mark the current
commit as bad (`git bisect bad`), then check out `HEAD~50` (i.e., 50 commits
ago):

<pre><code>guess which commit is first good commit (hash, branch, or a number of commits back): <strong>50</strong>
git bisect start
git bisect bad
git checkout HEAD~50
&gt; Note: checking out 'HEAD~50'.
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
&gt; HEAD is now at 40bafc4 Update the widget

hint: test this commit to see if it is good or bad:
  ibisect&gt; run make clean &amp;&amp; make &amp;&amp; make test

ibisect (no good)&gt;</code></pre>

Note that the `ibisect` prompt shows `(no good)`, not as an existential
reference to software in general, but to let you know that no commits have
yet been marked as "good".

To find out if this commit is good, you could use `ctrl-z` to background
`ibisect` then run the tests manually, but it's often easier to use `ibisect`'s
`run` command:

<pre><code>ibisect (no good)&gt; <strong>run rm -r node_modules; npm install; npm run test</strong>
rm -r node_modules; npm install; npm run test
...
Tests passed!
'rm -r node_modules; npm install; npm run test' exited with status 0
mark this commit as good [Y/n]:</code></pre>

Because the tests passed (exited with a status of 0), `ibisect` asks whether
this commit should be marked as good:

<pre><code>mark this commit as good [Y/n]: <strong>y</strong>
git bisect good
> Bisecting: 78 revisions left to test after this (roughly 6 steps)
> [6bc84f5e8d2091f34c8e7deddb25a45500e96fe6] Make the button red</code></pre>

Behind the scenes, `git bisect good` is called, which marks the commit as being
good. Now that git has both good and bad commits, it can start the process
of bisecting between the two. `git` lets us know that there are 78 commits
between the good and bad commits, it will take approximately 6 bisect steps
to walk through them, and `6bc84f...` is the next commit that needs to be
checked. It has also, conveniently, checked out that commit for us.

(Note that, even though we checked out `HEAD~50` - 50 commits back - there are
more than 50 commits to check because some branches were merged as part of
those 50 commits, and the commits in those branches may need to be checked.)

After the commit is marked as good, `ibisect` will re-run the tests, and prompt
again to ask whether the commit is good:

<pre><code>mark this commit as good [Y/n]: y
git bisect good
> Bisecting: 78 revisions left to test after this (roughly 6 steps)
> [6bc84f5e8d2091f34c8e7deddb25a45500e96fe6] Make the button red
rm -r node_modules; npm install; npm run test
...
Tests passed!
'rm -r node_modules; npm install; npm run test' exited with status 0
mark this commit as good [Y/n]: <storng>y</storng>
git bisect good
> Bisecting: 19 revisions left to test after this (roughly 4 steps)
> [c1fb14666a830a238deda8a75fc32d853ab7369c] Add a popup hint</code></pre>

Now there are only 19 commits left to check!

<pre><code>rm -r node_modules; npm install; npm run test
...
Tests failed!
'rm -r node_modules; npm install; npm run test' exited with status 1
mark this commit as bad [Y/n]:</code></pre>

Because the test suite failed this time, `ibisect` prompts to mark this commit
as being bad:

<pre><code>mark this commit as bad [Y/n]: <strong>y</strong>
git bisect bad
> Bisecting: 9 revisions left to test after this (roughly 3 steps)
> [c734f65cbffac961cd5bfb23737633f1a25d128c] Fix missing comma</code></pre>

And the testing continues:

<pre><code>rm -r node_modules; npm install; npm run test
...
npm: download failed!
'rm -r node_modules; npm install; npm run test' exited with status 1
mark this commit as bad [Y/n]: <strong>y</strong>
git bisect bad</code></pre>

This time, the `npm install` failed with an unrelated error, but it was
accidentally marked as being bad. To correct this, we'll use `ctrl-c` to cancel
the test, reply with `n` to return to the `ibisect` prompt:

<pre><code>git bisect bad
rm -r node_modules; npm install; npm run test
...
^C
'rm -r node_modules; npm install; npm run test' exited with status 1
mark this commit as bad [Y/n]: <strong>n</strong>
ibisect (~4 commits)&gt;</code></pre>

Then use `undo` to undo the last action:

<pre><code>ibisect (~4 commits)&gt; <strong>undo</strong>
undoing: git bisect bad c734f65cbffac961cd5bfb23737633f1a25d128c
git bisect start
git bisect bad a1fdfcd24b3d668b26c19d97719da669f15d34bf
git bisect good 2f892f37f97e5b8505c4ecf179b6638cddfc2361
git bisect good c4dcac6a151c42dcec08e1896208f69ff3e04ef6
git bisect good 15257bdbc988926a1bf44936ec582922aa946037
git bisect bad c1fb14666a830a238deda8a75fc32d853ab7369c
ibisect (~9 commits)&gt;</code></pre>

(Because git bisect doesn't natively support `undo`, it's implemented in
`ibisect` by restarting the bisect then re-running the log of good and bad
commits.)

Since this commit doesn't build and the test suite doesn't even start, it's
unclear whether this commit is good or bad. In this case, we'll `skip` the
commit:

<pre><code>ibisect (~9 commits)&gt; <strong>skip</strong>
git bisect skip
> Bisecting: 9 revisions left to test after this (roughly 3 steps)
> [03bde5e84afb32918c95d1a3283b9a145ec8d15b] Fix users table
ibisect (~9 commits)&gt;</code></pre>

Then press `ctrl-r` to start a reverse search, and type `run` to re-run the
tests:

<pre><code>(reverse-i-search)`run': rm -r node_modules; npm install; npm run test
rm -r node_modules; npm install; npm run test
...
Tests passed!
'rm -r node_modules; npm install; npm run test' exited with status 0</code></pre>

And let the tests run for a few more iterations, until finally:

<pre><code>...
Tests failed!
'rm -r node_modules; npm install; npm run test' exited with status 1
mark this commit as bad [Y/n]: <strong>y</strong>
git bisect bad
> 1555e0aa050d1cd538a1c9b8533909de3f7246b0 is the first bad commit
> commit 1555e0aa050d1cd538a1c9b8533909de3f7246b0
> Author: David Wolever <david@wolever.net>
> Date:   Wed Jan 30 14:23:49 2019 -0800
>
>     Fix broken package
>
> :040000 040000 66e8d3faee57d1d35259e1a86b582c141d02db18 64a1154d9048b8539df4dc2b7299ebfe3990f416 M	package.json
ibisect (finished 1555e0aa)&gt;</code></pre>

We've found the first bad commit!

<pre><code>ibisect (finished 1555e0aa)&gt; <strong>show</strong>
git show
> commit 1555e0aa050d1cd538a1c9b8533909de3f7246b0
> Author: David Wolever <david@wolever.net>
> Date:   Wed Jan 30 14:23:49 2019 -0800
>
>     Fix broken package
>
> diff --git a/package.json b/package.json
> index 6bfa23160..aecfba6e8 100644
> --- a/package.json
> +++ b/package.json
> @@ -294,12 +294,12 @@
>    "redux": "^3.5.2",
>    "redux-auth-wrapper": "^2.0.2",
>    "redux-logic": "^0.12.3",
>    "redux-saga": "^0.16.0",
>    "restyped-axios": "^1.3.1",
> -  "timsort": "^0.2.0",
> +  "timsort": "^0.3.0",
>    "ts-loader": "^3.3.1",
>    "ts-node": "^5.0.0",
>    "tslint-eslint-rules": "^4.1.1",
>    "tslint-react": "^3.4.0",
>    "typescript": "=3.2.2",</code></pre>

Finally, we'll `reset` the bisect, which will check out the branch we were
working from when the bisect started:

<pre><code>ibisect (finished 1555e0aa)&gt; <strong>reset</strong>
git bisect reset
> Previous HEAD position was 3d6f9fed2 Fix unmute button hover
> Switched to branch 'master'
> Your branch is up to date with 'origin/master'.
ibisect (not bisecting)&gt; <strong>exit</strong></code></pre>

And we can fix the bug, commit, and carry on like normal.

Tip: `git bisect` will create a reference to the first bad commit -
`bisect/bad` - which can be shown and checked out:

<pre><code>[master] $ <strong>git checkout bisect/bad</strong>
Note: checking out 'bisect/bad'.

You are in 'detached HEAD' state. You can look around, make experimental
changes and commit them, and you can discard any commits you make in this
state without impacting any branches by performing another checkout.

If you want to create a new branch to retain commits you create, you may
do so (now or later) by using -b with the checkout command again. Example:

  git checkout -b &lt;new-branch-name>

HEAD is now at 1555e0aa Fix broken package</code></pre>


Installation
============

Manually:

    $ curl https://raw.githubusercontent.com/wolever/git-ibisect/master/git-ibisect -O /usr/local/bin/git-ibisect
    $ chmod +x /usr/local/bin/git-ibisect

TODO
====

- Documentation:
  - Introduction which describes what bisect is and how it works
  - Better walkthrough of using ibisct
- Handle bisecting when starting from a dirty state (ex, prompt to `git stash`?)
- Figure out how to write tests
- Tab completion of filenames when using `run` and `autorun`
- Make sure ^C is handled well:
  - When running tests: should prompt "was this commit/bad/ignore?"
  - When prompting for input: should return to command line
- Add option to skip commit
- Allow bisect options to be passed from the command line:
  - `git ibisect reset`
  - `git ibisect undo`
  - etc
- Allow commits to be specified by age (ex, "10 days ago")
