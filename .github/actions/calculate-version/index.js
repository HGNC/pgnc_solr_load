#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');
const { resolveNextVersion, parseVersion, compareSemver } = require('./lib/version-utils.js');

async function fetchTags({ owner, repo, token, apiBase }) {
  const tags = [];
  let page = 1;
  const perPage = 100;

  while (true) {
    const url = `${apiBase}/repos/${owner}/${repo}/tags?per_page=${perPage}&page=${page}`;
    const response = await fetch(url, {
      headers: {
        'Authorization': `token ${token}`,
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'GitHub-Actions'
      }
    });

    if (!response.ok) {
      throw new Error(`GitHub API error: ${response.status} ${response.statusText}`);
    }

    const batch = await response.json();
    if (batch.length === 0) break;

    tags.push(...batch.map(t => t.name));
    if (batch.length < perPage) break;
    page++;
  }

  return tags;
}

function findLatestSemverTag(tags) {
  const semverTags = tags
    .map(tag => {
      try {
        return parseVersion(tag);
      } catch {
        return null;
      }
    })
    .filter(Boolean);

  if (semverTags.length === 0) return null;

  return semverTags.reduce((latest, current) =>
    compareSemver(current.normalized, latest.normalized) > 0 ? current : latest
  );
}

function setOutput(name, value) {
  const outputFile = process.env.GITHUB_OUTPUT;
  if (!outputFile) {
    console.log(`::set-output name=${name}::${value}`);
    return;
  }
  fs.appendFileSync(outputFile, `${name}=${value}\n`, 'utf8');
}

async function main() {
  try {
    const token = process.env.GITHUB_TOKEN;
    const releaseType = process.env.INPUT_RELEASE_TYPE || 'patch';
    const explicitVersion = process.env.INPUT_EXPLICIT_VERSION || '';
    const repository = process.env.GITHUB_REPOSITORY;
    const apiBase = process.env.GITHUB_API_URL || 'https://api.github.com';

    if (!token) throw new Error('GITHUB_TOKEN environment variable is required');
    if (!repository) throw new Error('GITHUB_REPOSITORY environment variable is required');

    const [owner, repo] = repository.split('/');
    const tags = await fetchTags({ owner, repo, token, apiBase });

    const latestTag = findLatestSemverTag(tags);
    const currentTag = latestTag ? latestTag.normalized : '';

    const result = resolveNextVersion({ currentTag, releaseType, explicitVersion });

    setOutput('next_version', result.nextVersion);
    setOutput('is_bootstrap', result.isBootstrap);
    setOutput('previous_version', result.previousVersion);
    setOutput('release_strategy', result.releaseStrategy);
    setOutput('resolved_release_type', result.resolvedReleaseType);

  } catch (error) {
    console.error('Error:', error.message);
    process.exit(1);
  }
}

main();
