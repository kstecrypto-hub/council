# Publication record

## Current GitHub repository

The owner created the private repository `kstecrypto-hub/council` and supplied its URL. The approved design and supporting documentation were then committed to `main` through the connected GitHub file operations, preserving the owner's initial README commit.

The complete specification was published in commit `f159423dafba71cf4334bd2a6cc6424bf6178587`. Its Git blob hash is `5a6ad97e389e10fb24e7e48239c96284fe12ed78`, matching the prepared design export exactly.

The repository contains the complete app design, implementation handoff, agent instructions, references, repository hygiene files, and publication/verification records. The app itself has not been built.

## Earlier archive and helper

The earlier `council-design-repository.zip` was a locally committed export prepared before this remote repository existed. Its local commit hash is not the commit hash of this GitHub publication. Do not force-push the archive over the existing remote history to make them match.

The archive's claim that the GitHub connection was read-only was incorrect. The available connection supported file writes but did not expose repository creation. The owner created the repository; the documentation was uploaded afterward.

`publish.ps1` is retained from that export. It is an optional helper for creating a separately authorized NEW private repository from an appropriately prepared local working tree. It is not an application launcher or an updater for this existing repository.

**Do not run the helper to recreate `kstecrypto-hub/council`; it already exists.** The helper intentionally refuses existing remotes and does not overwrite an existing repository or force-push. It has not been executed as part of this publication.

Future changes should use the existing repository and normal reviewed commits. No access tokens belong in the documentation or conversation.
