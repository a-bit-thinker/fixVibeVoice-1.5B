# Rollback Guide

This workspace is versioned with Git tags.  
Release tag for this setup: `v0.2.0`.

## Check current version

```bash
cd /root/fish-speech/VibeVoice
cat VERSION
git describe --tags --always
```

## Roll back safely (recommended)

Create a rollback branch from the release tag:

```bash
cd /root/fish-speech/VibeVoice
git switch -c rollback-v0.2.0 v0.2.0
```

This keeps your current branch unchanged.

## Return to your main working branch

```bash
cd /root/fish-speech/VibeVoice
git switch main
```
