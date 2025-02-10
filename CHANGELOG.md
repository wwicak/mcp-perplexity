# CHANGELOG



## v0.3.1 (2025-02-10)

### Fix

* fix: package naming and version ([`cf29a51`](https://github.com/daniel-lxs/mcp-perplexity/commit/cf29a511a02a6c3e3f33e346e6dcfbab87925355))


## v0.3.0 (2025-02-10)

### Chore

* chore: Bump project version to 0.3.0 ([`35c981b`](https://github.com/daniel-lxs/mcp-perplexity/commit/35c981b56e70648cc7b8021dd8b12ada567d18a8))

### Ci

* ci: Enable manual workflow dispatch for PyPI package publishing ([`f8a48ad`](https://github.com/daniel-lxs/mcp-perplexity/commit/f8a48adbd504cf327e71243e7f77c499b199203f))

### Documentation

* docs: Revamp README with comprehensive installation and configuration guide

- Remove Smithery installation section
- Add detailed uvx installation instructions for Windows and Unix systems
- Enhance MCP client configuration documentation
- Include more detailed environment variable explanations
- Add link to Perplexity model documentation ([`b8a5a86`](https://github.com/daniel-lxs/mcp-perplexity/commit/b8a5a86bac65fdd0d7e0127ec8aa2c6a4e77b2a8))

### Feature

* feat: Add configuration options for Perplexity model and chat database ([`1228278`](https://github.com/daniel-lxs/mcp-perplexity/commit/12282788e4f586e424eaaa1ca72fb9c8e9644085))

### Refactor

* refactor: Update MCP start command and add Dockerfile configuration ([`56cebde`](https://github.com/daniel-lxs/mcp-perplexity/commit/56cebde6e35c2c04cf4cdfba6acf6494db4b7b28))

* refactor: Enhance Dockerfile for development and runtime configuration ([`b06a8fa`](https://github.com/daniel-lxs/mcp-perplexity/commit/b06a8fa8f9c30e68e14a6174eb89481bcb4c0a5c))

* refactor: Optimize Dockerfile and dependency management

- Update Dockerfile to use multi-stage build with more efficient dependency installation
- Improve virtual environment setup and package installation process
- Add Hatch build configuration in pyproject.toml
- Update uv.lock with latest dependency versions ([`c406e59`](https://github.com/daniel-lxs/mcp-perplexity/commit/c406e59a632e53a1a3d63f733dc6b472f5b97a5c))

### Unknown

* Update README.md ([`5864df2`](https://github.com/daniel-lxs/mcp-perplexity/commit/5864df292d962e27735807f4e83b2bfa89e19c17))

* Update README.md ([`2a1f6ab`](https://github.com/daniel-lxs/mcp-perplexity/commit/2a1f6ab376d0f1148d8dd36890bb1155f2b6fbaf))


## v0.2.1 (2025-02-06)

### Chore

* chore: Bump project version to 0.2.1 ([`862ed70`](https://github.com/daniel-lxs/mcp-perplexity/commit/862ed708aab049ac212c6b55f92825247682df19))

* chore: Update release workflow permissions configuration

- Move permissions to top-level workflow configuration
- Add explicit write permissions for contents, actions, and id-token ([`d4e16f7`](https://github.com/daniel-lxs/mcp-perplexity/commit/d4e16f70506eb7d8c4498b42317f54ebe03ada73))

### Documentation

* docs: Update README with improved feature descriptions and model information ([`a92e563`](https://github.com/daniel-lxs/mcp-perplexity/commit/a92e563e1432d898e562dd88543aa665262cbf62))

* docs: Update Glama.ai server badge URL in README ([`1565bf0`](https://github.com/daniel-lxs/mcp-perplexity/commit/1565bf01bc3b36e469b6b1ba4548f3d46dd84852))

* docs: Add PyPI publish workflow badge to README ([`ad4de00`](https://github.com/daniel-lxs/mcp-perplexity/commit/ad4de0026e8c096fddfb62ac12cf20057fa5c27f))


## v0.2.0 (2025-02-06)

### Chore

* chore: Update artifact upload configuration in release workflow

- Upgrade actions/upload-artifact to v4
- Add retention-days and compression-level settings
- Ensure error handling for missing distribution files ([`bea6336`](https://github.com/daniel-lxs/mcp-perplexity/commit/bea633666e6621b52d1b23c63d454d138f56c7a9))

* chore: Optimize GitHub Actions release workflow for semantic release ([`700bb61`](https://github.com/daniel-lxs/mcp-perplexity/commit/700bb619d05df7bfc204873129954955a015bfda))

* chore: Improve Hatch installation and verification in GitHub Actions workflow ([`feebf4a`](https://github.com/daniel-lxs/mcp-perplexity/commit/feebf4a1c25924def776c76aefabc725601d41d6))

* chore: Adjust Hatch build and GitHub Actions configuration

- Update pyproject.toml to use explicit Python command for Hatch build
- Add Hatch to PATH in GitHub Actions workflow ([`096dd8c`](https://github.com/daniel-lxs/mcp-perplexity/commit/096dd8c8008ac8433f32c46da58aba5dfed43e8d))

* chore: Update Hatch GitHub Action to latest version ([`3bd663d`](https://github.com/daniel-lxs/mcp-perplexity/commit/3bd663de613d94e95bc956d110dbae1f1596e475))

* chore: Refine release workflow Hatch integration ([`91949e0`](https://github.com/daniel-lxs/mcp-perplexity/commit/91949e01adc2736aa351dce3d363b5927842c5c0))

* chore: Update build and release workflow to use Hatch ([`15468d5`](https://github.com/daniel-lxs/mcp-perplexity/commit/15468d58717757f509b532b86699aaa11772ffbb))

* chore: Configure semantic release for automated versioning and GitHub releases ([`6c0a6cc`](https://github.com/daniel-lxs/mcp-perplexity/commit/6c0a6ccaad58c4bee60d7fbf0fcfcfc49c39e2e7))

* chore: Update VSCode configuration in .gitignore ([`c33ac58`](https://github.com/daniel-lxs/mcp-perplexity/commit/c33ac58e00bc163fba8f682ffedd1f056d0614e6))

* chore: Remove VSCode Python settings file ([`e956e37`](https://github.com/daniel-lxs/mcp-perplexity/commit/e956e37c45917b6c2a90b84d0a0471fa3486f846))

### Documentation

* docs: Update mcp-server-starter reference to mcp-starter in README ([`3462012`](https://github.com/daniel-lxs/mcp-perplexity/commit/34620126be7fc41a13adcddebd3ea8d78d2fe1cf))

### Feature

* feat: Enhance database initialization with robust error handling and path support

- Add support for configurable database path via PERPLEXITY_DB_PATH
- Implement directory creation for database file
- Improve error handling during database initialization
- Use os.path for more flexible path management ([`42150e5`](https://github.com/daniel-lxs/mcp-perplexity/commit/42150e5139a7c5842023ce3365ac7023febe0a01))

### Fix

* fix: lower the amount of numbers generated for chat ids ([`2dc5e01`](https://github.com/daniel-lxs/mcp-perplexity/commit/2dc5e013a152e4aed0d0b2706cd8d4b967691107))

* fix: remove invalid property from progress notification ([`51673ef`](https://github.com/daniel-lxs/mcp-perplexity/commit/51673efecd536a3161bbf3849fe4f22df34bc30f))

### Refactor

* refactor: Simplify system prompt and improve code formatting

- Extract system prompt to a constant for reusability
- Remove redundant system prompt definition
- Improve code formatting and consistency
- Reduce code duplication in tool handling methods ([`3750cf6`](https://github.com/daniel-lxs/mcp-perplexity/commit/3750cf64526199783e312667123c662bb27c7d29))

### Unknown

* Merge pull request #2 from smithery-ai/smithery/config-1kti

Deployment: Dockerfile and Smithery config ([`d2af737`](https://github.com/daniel-lxs/mcp-perplexity/commit/d2af737520c7c85c628bba9a11402beaf6d3378b))


## v0.1.2 (2025-02-05)

### Chore

* chore: Bump version to 0.1.2 ([`db10e3f`](https://github.com/daniel-lxs/mcp-perplexity/commit/db10e3f739ee3101d2c0a5eb7c939dc5f5acac80))

### Documentation

* docs: Update README with new Perplexity model configuration details ([`b19ff40`](https://github.com/daniel-lxs/mcp-perplexity/commit/b19ff4008d00383e9bd385952a547aaa4f950346))

### Feature

* feat: Add configurable Perplexity models for ask and chat tools

- Introduce PERPLEXITY_MODEL_ASK and PERPLEXITY_MODEL_CHAT environment variables
- Allow separate model selection for ask and chat tools
- Fallback to default PERPLEXITY_MODEL if specific models are not set
- Increase chat ID token length for more unique identifiers ([`904cf82`](https://github.com/daniel-lxs/mcp-perplexity/commit/904cf82a13c8f9ed845bccc13d1f5173480f93ae))

### Unknown

* Update README ([`d970805`](https://github.com/daniel-lxs/mcp-perplexity/commit/d9708058080e0167e5d6c48dc945c29b0915ff85))

* Add Smithery configuration ([`324cc07`](https://github.com/daniel-lxs/mcp-perplexity/commit/324cc0755407eddd5a29c249e15417ef3c5cd349))

* Add Dockerfile ([`c5c624d`](https://github.com/daniel-lxs/mcp-perplexity/commit/c5c624d67283ae15acefed055a8cc92ec933c6f4))


## v0.1.1 (2025-02-05)

### Chore

* chore: Bump version to 0.1.1 ([`99b8bc7`](https://github.com/daniel-lxs/mcp-perplexity/commit/99b8bc70f193071f701aa3ada4b5428aac625628))

* chore: make version match release ([`996739a`](https://github.com/daniel-lxs/mcp-perplexity/commit/996739ad688a247e23f26e7e2b405cba3ba8492e))

* chore: Remove Hirofumi Tanigami from project authors ([`9c80a0a`](https://github.com/daniel-lxs/mcp-perplexity/commit/9c80a0acd8537efa4289fa2480d2f39b54c368c0))

* chore: Add PyPI publish GitHub Actions workflow ([`ca8e5dc`](https://github.com/daniel-lxs/mcp-perplexity/commit/ca8e5dcd48a95094e23b14e2f090429861f3f146))

* chore: rename package to mcp-perplexity ([`3c6fbe6`](https://github.com/daniel-lxs/mcp-perplexity/commit/3c6fbe6100f392a63351cef35e7ef8514a3acf36))

* chore: Update project metadata and version

- Bump version from 0.1.2 to 0.2.3
- Add Daniel Riccio as a project author ([`f8b98fd`](https://github.com/daniel-lxs/mcp-perplexity/commit/f8b98fdaa46f1a28aef3dcf8c57c12107a6fdc21))

### Documentation

* docs: Update README with comprehensive installation instructions for MCP server ([`3fd6c1a`](https://github.com/daniel-lxs/mcp-perplexity/commit/3fd6c1a5511585ae825a965f2583d524cb527137))

* docs: Update MCP client configuration instructions in README ([`8314f4a`](https://github.com/daniel-lxs/mcp-perplexity/commit/8314f4ae56bb6a3c9c856f2e1ad712bcfa064584))

* docs: Update project repository and README with new features and installation instructions ([`0570610`](https://github.com/daniel-lxs/mcp-perplexity/commit/05706108253589d977af0e72d2b0cbb1077262b7))

### Feature

* feat: Add persistent chat functionality and database storage

- Implement chat history tracking with SQLite database
- Add new `chat_perplexity` tool for maintaining conversation context
- Introduce chat ID generation and message storage
- Enhance progress tracking for chat responses
- Update dependencies to include `haikunator` and `httpx`
- Bump version to 0.2.5 ([`a56c875`](https://github.com/daniel-lxs/mcp-perplexity/commit/a56c8753c04b2578527ebd7bfd1924bde1e1d73b))

* feat: Enhance Perplexity tool with streaming response and improved error handling

- Refactored Perplexity API interaction to support streaming responses
- Added robust JSON parsing for API chunks
- Implemented progress tracking and detailed response formatting
- Added system prompt to guide response generation
- Improved error handling and logging
- Updated tool input schema for more focused querying ([`bdce645`](https://github.com/daniel-lxs/mcp-perplexity/commit/bdce64515fba45f614c60c3053bdb32cf30cdd32))

### Fix

* fix: add note about timeout to README ([`e332ed3`](https://github.com/daniel-lxs/mcp-perplexity/commit/e332ed322a9dd29b4edd44f1ca5bd61131405dce))

### Test

* test: Add comprehensive Perplexity API test suite ([`c7a4327`](https://github.com/daniel-lxs/mcp-perplexity/commit/c7a43276d5b67c58f98539636fe0bba431c0e118))

### Unknown

* Merge pull request #2 from smithery-ai/add-smithery

Add Smithery to README ([`ad27eec`](https://github.com/daniel-lxs/mcp-perplexity/commit/ad27eec59a20f0334972ce99c913aaccc29d92e8))

* Add Smithery CLI installation instructions and badge ([`4baaaf7`](https://github.com/daniel-lxs/mcp-perplexity/commit/4baaaf7c22c21f0897f078c9ad76073cb3c7334e))

* Create LICENSE ([`c2cd77d`](https://github.com/daniel-lxs/mcp-perplexity/commit/c2cd77d31523fd837e035ad89e3b332aeefbc815))

* Merge pull request #1 from punkpeye/patch-1

add MCP server badge ([`50a2741`](https://github.com/daniel-lxs/mcp-perplexity/commit/50a2741ab4e95a2e81c340a37278ec94669d1340))

* add MCP server badge

This PR adds a badge for the Perplexity MCP Server server listing in Glama MCP server directory.

&lt;a href=&#34;https://glama.ai/mcp/servers/hchfq9bydq&#34;&gt;&lt;img width=&#34;380&#34; height=&#34;200&#34; src=&#34;https://glama.ai/mcp/servers/hchfq9bydq/badge&#34; alt=&#34;Perplexity Server MCP server&#34; /&gt;&lt;/a&gt;

Glama performs regular codebase and documentation scans to:

* Confirm that the MCP server is working as expected
* Confirm that there are no obvious security issues with dependencies of the server
* Extract server characteristics such as tools, resources, prompts, and required parameters.

This badge helps your users to quickly asses that the MCP server is safe, server capabilities, and instructions for installing the server. ([`aa9d40f`](https://github.com/daniel-lxs/mcp-perplexity/commit/aa9d40f9bbeff2d86f9b5eb729187373e1c8bfa0))

* Update README.md ([`0260c13`](https://github.com/daniel-lxs/mcp-perplexity/commit/0260c13b1d5081c6309d459be0e7cbb50b238a95))

* first commit ([`4253ab6`](https://github.com/daniel-lxs/mcp-perplexity/commit/4253ab62524d06f7aa5209e74b995429c6db45b8))
