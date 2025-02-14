# Contributing to Cataclysm: The Last Generation

## Filing bug reports

Properly filled out bug reports are very welcome.
There are guided issue forms which aid in creation of good bug reports.

Before submitting one, check if this issue exists in our upstream, [Cataclysm: DDA](https://github.com/CleverRaven/Cataclysm-DDA).
We can backport fixes, should it be fixed there already. We are constantly backporting and will pull fixes eventually, so
reserve backport requests for urgent, game breaking fixes that need to be pulled out of order.

## Contributing code

### Helping with roadmap features

> [!CAUTION]
> This project does not accept *unsolicited* feature additions through PR. You will waste your time with this, as your PR will be closed.
> Unless you *specifically* got an approval for your addition, investing time into this will be futile and benefit no one.

Speeding up the development of the game with your contributions is possible, but you **must** discuss working on these features first, as
features will need to be implemented in certain ways and you must adhere to them. Undiscussed changes will be rejected.

### Assisting with backports

You are welcome to assist with backporting. See [BACKPORTING.md](BACKPORTING.md).

Please do not backport low-complexity changes unless in bulk. We have to review every single one and repeatedly filing PRs for typo
fixes is annoying. Pulling a typo or otherwise low severity fix from the future is also heavily discouraged as risking conflicts
and burdening the reviewers is not worth it for things like these.

However, we are very grateful for people to take care of complex or otherwise non-trivial backports, especially if done by the person
who originally contributed the fixes upstream.

### Maintaining documentation

We have removed most of the documentation as pointlessly duplicating DDA things makes things vastly harder and instead opted to
document differences. Documentation is a chore and we are thankful if someone offers to take care of it.

### Tileset additions

The DDA tilesets have gotten fixes and additions, but backporting them is very hard as git can not resolve merge conflicts in
binary files. If you are adept with graphics software and would like to give it your all, discuss it first.

### Fixing bugs

Bug fixes are appreciated, but you are encouraged to discuss your proposed fix first, especially if the fix will affect many lines of code.
It is possible something is not a bug but intentional and discussing things first would clear that up.
