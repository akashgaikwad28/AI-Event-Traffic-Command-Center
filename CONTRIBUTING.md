# Contributing to GridWise AI

First off, thank you for considering contributing to GridWise AI! It's people like you that make GridWise AI a great tool for smart city infrastructure.

## 1. Where do I go from here?

If you've noticed a bug or have a feature request, make sure to check our issues page to see if someone else in the community has already created a ticket. If not, go ahead and make one!

## 2. Fork & create a branch

If this is something you think you can fix, then fork GridWise AI and create a branch with a descriptive name.

A good branch name would be (where issue #325 is the ticket you're working on):

```shell
git checkout -b 325-add-new-dashboard-widget
```

## 3. Implementation and Testing

Please follow the [Development Guidelines](docs/DEVELOPMENT_GUIDELINES.md) to ensure your code aligns with our project standards.

Don't forget to run our test suite before submitting your PR!

## 4. Make a Pull Request

At this point, you should switch back to your master branch and make sure it's up to date with GridWise AI's master branch:

```shell
git remote add upstream git@github.com:akashgaikwad28/AI-Event-Traffic-Command-Center.git
git checkout main
git pull upstream main
```

Then update your feature branch from your local copy of main, and push it!

```shell
git checkout 325-add-new-dashboard-widget
git rebase main
git push --set-upstream origin 325-add-new-dashboard-widget
```

Finally, go to GitHub and make a Pull Request.

## 5. Keeping your Pull Request updated

If a maintainer asks you to "rebase" your PR, they're saying that a lot of code has changed, and that you need to update your branch so it's easier to merge.

## 6. Code of Conduct

By participating in this project, you agree to abide by the [Code of Conduct](CODE_OF_CONDUCT.md).
