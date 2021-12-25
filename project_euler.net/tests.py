class test:
	def __init__(self,pvrple,blvck):
		self.pvrple = pvrple
		self.blvck = blvck

	def test(pvrpleblvck):
		pass


# git branch <new-branch-name>
# git branch -m <new-name>
# git branch -m <old-name> <new-name>

# First, delete the current / old branch:
# git push origin --delete <old-name>

# Then, simply push the new local branch with the correct name:
# git push -u origin <new-name>

# git checkout <other-branch>
# git switch <other-branch>
# git push -u origin <local-branch>
# git branch --track <new-branch> origin/<base-branch>

# (1) Check out the branch that should receive the changes
# git switch main
	
# (2) Execute the "merge" command with the name of the branch that contains the desired changes
# git merge feature/contact-form

print('H')



#git remote add new-remote-repo https://hostname/user/repo.git
# Add remote repo to local repo config
#git push <new-remote-repo> test_branch~
# pushes the test_branch branch to new-remote-repo