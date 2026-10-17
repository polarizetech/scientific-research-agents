# Standard interface and small-app architecture

This is the default shared by Polarize research apps. It records an existing convention, not a new
framework choice.

## Design system

The organisation profile supplies `{{design_system}}`. In a Polarize installation that resolves to
[`polarizetech/polarize-ui`](https://github.com/polarizetech/polarize-ui), whose package name is
`@polarizetech/polarize-ui`.

Before designing or implementing an element:

1. read the pinned release's `README.md`, `METHOD.md`, integration guide, and Storybook;
2. search its public components, science views, layouts, tokens, custom elements, and CSS classes;
3. reuse the existing element without copying or locally restyling it;
4. if it is missing, add it to the design-system repository with a story and checks, release it, pin that
   release in the app, and only then consume it.

Never fork a design-system component or create a parallel app-local component that will drift. A temporary
prototype is visibly marked as such and cannot become the shipped implementation. Pin a release tag; do not
consume a moving branch or an unversioned checkout.

## Default small web app

The default research app is deliberately boring:

```text
apps/<slug>/vN/
  index.html
  app.js
  app.css
  serve.py
```

- `index.html`, `app.js`, and `app.css` stay zero-build unless a demonstrated requirement needs React or a
  build tool.
- `serve.py` is the single local entrypoint. Prefer the Python standard library
  (`ThreadingHTTPServer` plus a small explicit handler) for static files and modest JSON endpoints.
- Accept `PORT` from the environment; an explicit CLI port may take precedence when the repository already
  follows that convention. Bind to loopback by default unless deployment explicitly requires another
  interface.
- Serve design-system files and other shared browser dependencies through an allow-list of named files,
  never by mounting an external directory. Safe font prefixes are acceptable only when traversal is
  rejected.
- Locate dependencies through the repository's resolver, an environment variable, or a verified sibling
  checkout; never use an absolute home-directory path.
- Missing design assets produce a clear warning and an unstyled-but-usable app, not a silent fallback to a
  different design.
- Use `Cache-Control: no-store` in local research tools where stale data or design assets would mislead.
- Keep APIs under `/api/`, return explicit JSON errors and content types, and test the health/data paths.
- Persist nothing unless the app's scope explicitly requires it. Never expose a repository, corpus, raw
  recording directory, secret, or arbitrary path through the server.

## When the default is not enough

React is appropriate when interaction and state have outgrown the zero-build form. It still uses the pinned
`@polarizetech/polarize-ui` React exports and theme rather than an app-local component system. Vite may build
the browser bundle, but a research tool with local APIs keeps a Python server as its documented entrypoint
and serves the built assets plus `/api/` routes.

Use FastAPI, Flask, or another Python server only when requirements such as typed API schemas, streaming,
authentication, concurrency, or an existing repository stack justify the dependency. Record that reason.
Static-only hosting may omit the Python runtime in deployment, but local development and validation retain a
Python `serve.py` unless the repository's established convention says otherwise.

## Ownership and handoff

- The **designer** specifies existing design-system components and states; a missing element is a proposed
  design-system addition.
- The **frontend developer** creates the app shell, integrates the pinned components, implements browser
  behaviour, and supplies the default `serve.py` when it is only a static/data shim.
- The **computational engineer** owns non-trivial Python APIs, computation, persistence, streaming,
  authentication, and tests, agreeing the JSON contract with the frontend developer first.

The finished app records the design-system repository and tag, the command that starts it, its local URL,
its API routes, and the checks that were run.

## Basis in existing applications

This convention was checked against the scaffold protocol and representative apps including
`audio-evoked-potentials/apps/tuning-forks`, `matched-entropy-demodulation/apps/v15-visual-cortex`, and
`world-seeding/apps/primary-elements/v1`. They use Python stdlib servers, explicit asset maps or allow-lists,
environment-configurable paths/ports, and the shared Polarize design system. Repository-specific additions
do not change the default above.
