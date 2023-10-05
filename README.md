# How to test changes made to the repo
1. `git pull`
2. Install all dependencies (including recently added ones) with `pip3 install -r requirements.txt` or `pip install -r requirements.txt` for python versions before 3.x
3. If everything's present either python3 app.py or flask run should work, and click on the link (which should be 127.0.0.1)

## General workflow when comitting new code (note to self)
1. `git pull`
2. Install all dependencies (including recently added ones) with `pip3 install -r requirements.txt` or `pip install -r requirements.txt` for python versions before 3.x
3. Create a new branch and change into it with the command `git checkout -b BRANCH_NAME` (usually feature is the standard branch name)
4. Make sure that you're in the appropriate branch with the `git branch` command.
5. Do some basic change and commit as normal, and then (just for the first time) use `git push origin BRANCH_NAME`.
6. After that, treat the branch as a standard workflow with git adding, commiting and pushing.
7. Once you think the whole feature has been implemented (i.e. you've finished all your commits, and the code is working) got to github, and you should see a button at the top that say "Compare and Pull Request".
8. Open a pull request, writing comments describing the feature as appropriate.
9. Once done, if you have control, you can also be the reviewer for the pull request, or assign someone else to verify that the code works, and they can merge the pull request with the main branch.
10. Once merged, delete the branch (there'll be a button that allows you to do so once you've merged it, and if you're not merging, the reviewer will delete the branch)
11. Locally, in your terminal use `git checkout main` to go back to the local main branch.
12. Delete the temporary branch you created with `git branch -d BRANCH_NAME`.
13. `git pull` to ensure your local repo is synced up with the merged main branch.