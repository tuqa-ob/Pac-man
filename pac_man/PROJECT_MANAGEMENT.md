# Project Management

## 1. Team Organization

The project was developed by two team members. Tasks were divided according to each member's responsibilities, while important design and integration decisions were discussed together.

| Login | Main Responsibilities |
|---|---|
| `tobaidat` | Project structure and planning, configuration, game logic, player implementation, initial rendering, code integration and review, packaging, and documentation. |
| `sal-omar` | Level implementation, ghost implementation, front-end development, visual design, screens and buttons, and cheat mode. |

Both members collaborated on design decisions, resolving integration issues, and selecting the overall visual theme.

## 2. Development Timeline and Milestones

| Date | Milestone | Progress |
|---|---|---|
| 8 September | Project planning | `tobaidat` established the initial project structure. The team agreed on a work plan and organized the development steps. |
| 20 September | Configuration | `tobaidat` completed the initial configuration file. |
| 27 September | Level implementation | `sal-omar` completed the initial `level.py` implementation. |
| 29 September | Initial game logic | `tobaidat` and `sal-omar` completed the initial versions of `game.py` and `player.py`. `sal-omar` also completed `ghost.py`. |
| 5–8 October | Code integration | Development of new features was paused to review and resolve overlapping responsibilities and inconsistencies between `game.py` and `level.py`. On 8 October, the latest updates were shared and a new coordination approach was agreed upon. |
| 10 October | Initial rendering | `tobaidat` completed a basic version of `render.py`. The game became playable with the player, ghosts, pac-gums, and super pac-gums displayed using simple visuals. |
| After 10 October | Front-end development | `sal-omar` developed the visual interface, including the menu, buttons, level transitions, win and game-over screens, high-score screen, and instructions screen. The team discussed design choices and selected the game's visual theme together. |
| 18 October | Code review and refinement | `tobaidat` reviewed the code, studied the implementations developed by `sal-omar`, and worked on correcting errors and addressing missing requirements. `sal-omar` implemented cheat mode. |
| 25 October | Game completion | The team completed the game implementation. |
| 25–31 October | Packaging and documentation | `tobaidat` worked on packaging the game and preparing the README and project management documentation. |
| 2 November (planned) | Submission | The original target was 29 October. Since packaging took longer than expected, the team agreed to move the planned submission date to Monday, 2 November. |

## 3. Workflow and Progress Tracking

The project followed a step-by-step development process. Each major component was initially assigned to one team member, then integrated with the rest of the game.

The workflow included:

1. Establishing the project structure and development plan.
2. Implementing the configuration, level, player, game logic, and ghost components.
3. Reviewing and integrating separately developed components.
4. Building the initial playable version.
5. Developing the visual interface and additional features.
6. Reviewing the complete implementation and correcting issues.
7. Packaging the game and preparing the documentation.

Progress was tracked through completed components and shared code updates. During integration, the team identified the need to review shared code before starting new tasks. This became an important part of the workflow for the remainder of development.

## 4. Difficulties, Decisions, and Solutions

### 4.1 Code Integration and Overlapping Responsibilities

One of the main difficulties occurred when integrating `game.py` and `level.py`.

The two files had initially been developed separately. When `tobaidat` implemented `game.py`, `level.py` was still being developed by `sal-omar`. As a result, some responsibilities overlapped or were implemented differently. Examples included direction handling and determining pac-gum positions.

**Decision and solution:**

- New development was paused between 5 and 8 October.
- `tobaidat` carefully reviewed the implementation of `level.py`.
- The team discussed which functions and responsibilities should be kept, integrated, modified, or removed.
- The latest changes were shared on 8 October.
- The team agreed not to begin a new task before reviewing the latest shared code.

This helped reduce duplicated functionality and improve consistency between components.

### 4.2 Balancing Development with University Responsibilities

When the university semester began, `tobaidat` had less time available for development. To keep the project moving, `sal-omar` continued working on the front-end implementation while the team maintained communication and discussed design decisions together.

### 4.3 Packaging Time

The team initially planned to submit the project on 29 October. However, preparing and testing the packaged version took longer than expected.

**Decision:** The submission target was moved to Monday, 2 November, allowing additional time for packaging and final preparation.

### 4.4 Technical and Design Decisions

The team made several implementation and design decisions during development:

- The maze generation component was kept separate from the main game logic through an adapter, making integration with the game easier.
- The maze generator was configured with `perfect=False`.
- The visual theme and interface design were discussed and selected jointly.
- The team adopted a shared-code review step before starting new development tasks to reduce integration conflicts.

## 5. Risk Analysis

The following table summarizes the main risks identified from the development experience and the measures used or planned to address them.

| Risk | Possible Impact | Mitigation |
|---|---|---|
| Separately developed components may have overlapping responsibilities. | Integration problems, duplicated functions, and inconsistent behavior. | Review shared code and agree on component responsibilities before continuing development. |
| Limited time due to university commitments. | Delays in completing assigned tasks. | Divide responsibilities and allow the other team member to continue with independent tasks. |
| Packaging may take longer than expected. | Delay in the final submission. | Reserve time for packaging and testing, and adjust the submission schedule when necessary. |
| Bugs or missing requirements may remain in the final implementation. | Incomplete or incorrect game behavior. | Conduct a code review and test the implemented features before submission. |

## 6. Testing and Acceptance Plan

The following acceptance checklist summarizes the main areas to verify.

- [x] The game launches successfully using the documented launch instructions.
- [x] The configuration file loads correctly.
- [x] Missing or invalid configuration values are handled using defaults and warnings.
- [x] The player can move and interact with the maze.
- [x] Ghosts behave as expected during gameplay.
- [x] Pac-gums and super pac-gums can be collected and update the score correctly.
- [x] Super pac-gum effects work as intended.
- [x] Collisions between the player and ghosts produce the expected results.
- [x] Level transitions work correctly.
- [x] Win and game-over conditions are displayed correctly.
- [x] High scores are displayed and saved as intended.
- [x] Menu buttons and navigation work correctly.
- [x] Instructions and cheat mode are accessible and function as intended.
- [x] The packaged version runs with its required assets.


## 7. Blocking Points and Lessons Learned

The main development blocker was the integration issue between `game.py` and `level.py`. It temporarily interrupted feature development and required the team to review the existing code before proceeding.

The experience highlighted several lessons:

- Dividing tasks is useful, but shared responsibilities and interfaces must be agreed upon early.
- Reviewing the latest shared code before starting new work can prevent unnecessary duplication.
- Integration should be treated as a continuous part of development rather than something left until the end.
- Packaging and documentation require dedicated time in the project schedule.
- Regular communication helps the team make consistent technical and design decisions.

## 8. Tools and Collaboration

- **GitHub:** Used for version control and sharing project code between team members.
- **Python and Pygame:** Used to implement the game.
- **PyInstaller:** Used to package the game into an executable distribution.
- **Shared discussions and code reviews:** Used to coordinate responsibilities, resolve integration issues, and agree on design decisions.
