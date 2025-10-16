'use strict';

const SEMVER_PATTERN = /^v?(\d+)\.(\d+)\.(\d+)$/;

function parseVersion(version) {
  const match = version.match(SEMVER_PATTERN);
  if (!match) {
    throw new Error(`Invalid semantic version: ${version}`);
  }

  const [, major, minor, patch] = match;
  return {
    normalized: `v${major}.${minor}.${patch}`,
    major: parseInt(major, 10),
    minor: parseInt(minor, 10),
    patch: parseInt(patch, 10)
  };
}

function normalizeVersion(version) {
  return version.startsWith('v') ? version : `v${version}`;
}

function normalizeReleaseType(releaseType) {
  const type = (releaseType || '').toLowerCase().trim();
  if (!type || type === 'patch') return 'patch';
  if (type === 'minor') return 'minor';
  if (type === 'major') return 'major';
  throw new Error(`Unsupported release_type: ${releaseType}. Must be patch, minor, or major.`);
}

function compareSemver(v1, v2) {
  const p1 = parseVersion(v1);
  const p2 = parseVersion(v2);

  if (p1.major !== p2.major) return p1.major - p2.major;
  if (p1.minor !== p2.minor) return p1.minor - p2.minor;
  return p1.patch - p2.patch;
}

function incrementVersion(version, releaseType) {
  const type = normalizeReleaseType(releaseType);
  if (type === 'major') return `v${version.major + 1}.0.0`;
  if (type === 'minor') return `v${version.major}.${version.minor + 1}.0`;
  return `v${version.major}.${version.minor}.${version.patch + 1}`;
}

function resolveNextVersion({ currentTag, releaseType, explicitVersion }) {
  if (!currentTag) {
    return {
      nextVersion: 'v1.0.0',
      isBootstrap: true,
      previousVersion: '',
      releaseStrategy: 'bootstrap',
      resolvedReleaseType: 'major'
    };
  }

  const current = parseVersion(currentTag);

  if (explicitVersion) {
    const explicit = parseVersion(normalizeVersion(explicitVersion));
    if (compareSemver(explicit.normalized, current.normalized) <= 0) {
      throw new Error(
        `explicit_version (${explicit.normalized}) must be greater than current version (${current.normalized})`
      );
    }
    return {
      nextVersion: explicit.normalized,
      isBootstrap: false,
      previousVersion: current.normalized,
      releaseStrategy: 'explicit',
      resolvedReleaseType: 'explicit'
    };
  }

  const type = normalizeReleaseType(releaseType);
  const nextVersion = incrementVersion(current, type);

  return {
    nextVersion,
    isBootstrap: false,
    previousVersion: current.normalized,
    releaseStrategy: releaseType === 'patch' ? 'auto' : 'override',
    resolvedReleaseType: type
  };
}

module.exports = {
  SEMVER_PATTERN,
  parseVersion,
  normalizeVersion,
  normalizeReleaseType,
  compareSemver,
  incrementVersion,
  resolveNextVersion
};
