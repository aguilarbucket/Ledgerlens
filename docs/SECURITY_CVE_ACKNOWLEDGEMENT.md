# Security CVE risk acknowledgement

## Decision

LedgerLens temporarily accepts the inherited Debian `perl-base` findings described below for the
OpenAI Build Week 2026 demonstration. This is a time-bounded demo acceptance, not a statement that
the CVEs are fixed and not an authorization for production or multi-user internet deployment.
Docker Scout exceptions are not used to hide or suppress the findings.

- Accepted by: project owner
- Acceptance date: 2026-07-19
- Review no later than: 2026-08-18
- Reopen sooner if Debian publishes a fixed Trixie package, the base image changes, LedgerLens
  begins invoking Perl or processing ZIP/glob input, or the application is considered for hosted,
  production, or multi-user use.

## Evaluated artifact

- Image: `alejandroromeroa/ledgerlens:buildweek-2026`
- Manifest digest:
  `sha256:785085e8c1540dbb2a6125a219b2b1bd2a1c62566bb249ac55efe751411ba513`
- Image source revision: `d89a59e3d4dd75838c1da4397e76f965de4a9ef1`
- Platform: `linux/amd64`
- Base image detected by Scout: `python:3.13-slim` on Debian 13 Trixie
- Scan date: 2026-07-19
- Docker Scout CLI used for this review: 1.21.0

## Scan results

`docker scout quickview` reported `1 critical`, `2 high`, `3 medium`, `25 low`, and `7
unspecified` findings. Scout attributed the same totals to the base image.

These results were revalidated after publishing the auditable record-correction release. The
immutable `d89a59e` tag, `buildweek-2026`, and `latest` resolve to the evaluated digest above.

Two follow-up checks materially narrow the result:

- `docker scout cves --only-fixed`: zero fixable CVEs at every severity.
- `docker scout cves --ignore-base`: zero CVEs introduced by the LedgerLens application layer.

The critical and high findings are all attributed to Debian `perl-base 5.40.1-6`, an essential
package inherited from the official base image:

| CVE | Scout severity | Upstream behavior | LedgerLens exposure assessment |
| --- | --- | --- | --- |
| [CVE-2026-12087](https://security-tracker.debian.org/tracker/CVE-2026-12087) | Critical | Out-of-bounds heap read in Perl Socket input handling. | LedgerLens does not invoke Perl or pass user-controlled socket arguments to Perl. Debian Trixie still lists the package as vulnerable and has no fixed Trixie package. |
| [CVE-2026-48959](https://security-tracker.debian.org/tracker/CVE-2026-48959) | High | CPU exhaustion when Perl `IO::Uncompress::Unzip` seeks a named entry in an attacker-supplied ZIP. | LedgerLens accepts bounded PDF input, does not process ZIP files with Perl, and caps container CPU and memory in the documented runtime. Debian Trixie still lists the package as vulnerable. |
| [CVE-2026-48962](https://security-tracker.debian.org/tracker/CVE-2026-48962) | High | Arbitrary Perl evaluation through an attacker-controlled `File::GlobMapper` output glob. | LedgerLens does not invoke Perl, `File::GlobMapper`, shell commands, or user-controlled globs. The documented runtime is non-root, capability-free, read-only, and prevents privilege escalation. Debian Trixie still lists the package as vulnerable. |

The Debian tracker describes the relevant Trixie module issues as `no-dsa` minor issues, while the
scanner reports the severities above against the inherited `perl` package. Both facts are retained
rather than using the lower contextual rating to erase the scanner result.

## Patch availability assessment

An ephemeral `apt-get update` and `apt-cache policy perl-base` check returned:

- Installed version: `5.40.1-6`
- Candidate version: `5.40.1-6`
- Upgradable operating-system packages: none

`perl-base` is marked `Essential: yes` and `Priority: required`. Removing it or copying packages
from Debian unstable would weaken the supported base-image boundary and is not an appropriate demo
patch. Docker Scout also showed that moving from Python 3.13 slim to Python 3.14 slim retains the
same vulnerability totals. An Alpine migration was deliberately rejected for this demo because it
would change the libc and dependency compatibility surface rather than provide a small patch.

## Compensating controls

The documented Docker and Compose paths apply controls that reduce exposure and bound impact
without changing the application dependency set:

- Run as the existing unprivileged UID 999.
- Bind Streamlit only to `127.0.0.1` on the host.
- Use a read-only root filesystem with a bounded, `noexec`, `nosuid` `/tmp` tmpfs.
- Drop all Linux capabilities and set `no-new-privileges`.
- Limit the container to 256 PIDs, 2 CPUs, and 1 GiB of memory.
- Keep only `/app/runtime` writable through the named persistence volume.
- Accept only size-bounded PDF input with extension, MIME, header, and EOF checks; no ZIP path is
  present.
- Run the offline synthetic path by default, with no API key or private account required.

A validation container using all of these controls reached healthy state, returned HTTP 200 `ok`,
and retained UID 999. Its temporary container and volume were removed after the check.

## Ongoing response

Before a new release, rerun:

```console
docker scout quickview alejandroromeroa/ledgerlens:buildweek-2026
docker scout cves --only-severity critical,high alejandroromeroa/ledgerlens:buildweek-2026
docker scout cves --only-fixed alejandroromeroa/ledgerlens:buildweek-2026
```

When Debian or the official Python base publishes a fixed compatible package, rebuild the image,
run the complete offline test and container verification matrix, publish a new immutable tag and
digest, and close this acceptance record with the replacement evidence.
