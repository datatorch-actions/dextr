<h1 align="center">
  DEXTR Action
</h1>

<h4 align="center">Use of extreme points in an object (left-most, right-most, top, bottom pixels) as input to obtain precise object segmentation for images and videos.</h4>

<p align="center">
  <img alt="DataTorch Action" src="https://img.shields.io/static/v1?label=DataTorch%20Action&message=datatorch/dextr@v1&color=blueviolet">
  <img alt="Open Issues" src="https://img.shields.io/github/issues/datatorch-actions/dextr">
</p>

DEXTR explores the use of extreme points in an object (left-most, right-most,
top, bottom pixels) as input to obtain precise object segmentation for images
and videos. We do so by adding an extra channel to the image in the input of a
convolutional neural network (CNN), which contains a Gaussian centered in each
of the extreme points. The CNN learns to transform this information into a
segmentation of an object that matches those extreme points. We demonstrate the
usefulness of this approach for guided segmentation (grabcut-style), interactive
segmentation, video object segmentation, and dense segmentation annotation. We
show that we obtain the most precise results to date, also with less user input,
in an extensive and varied selection of benchmarks and datasets.

<p align="center">
  <img src="https://github.com/scaelles/DEXTR-PyTorch/blob/master/doc/github_teaser.gif" align="center" width=480 height=auto/>
</p>

- [Quick Start](#quick-start)
- [Action](#action)
  - [Inputs](#inputs)
  - [Outputs](#outputs)
- [User Guide](#user-guide)
  - [Prerequisites](#prerequisites)
  - [Agent Setup](#agent-setup)
    - [Creating Agent](#creating-agent)
    - [Adding Agent to Project](#adding-agent-to-project)
  - [Pipeline Setup](#pipeline-setup)
  - [Usage](#usage)
- [FAQ](#faq)
  - [Quick Debug Checklist](#quick-debug-checklist)

## Quick Start

```yaml
name: DEXTR

triggers:
  # Adds a button to the annotator.
  annotatorButton:
    name: "DEXTR"
    icon: brain
    # Annotator will prompt the user for 4 points before triggering the pipeline
    flow: 4-points

jobs:
  predict:
    # Properties about the trigger event can be accessed at 'event' property
    steps:
      - name: Download File
        action: datatorch/download-file@v1
        inputs:
          # Get the file id for the event that triggered this.
          fileId: ${{ event.fileId }}

      - name: Predict Segmentation
        action: datatorch/dextr@latest
        inputs:
          # Download file path from the previous action.
          imagePath: ${{ variable.path }}
          # Get the 4 points the user clicked
          points: ${{ event.flowData.points }}
          # Annotation created by the four points. We will insert the
          # segmentation into this annotation
          annotationId: ${{ event.annotationId }}
```

> **NOTE:** Running DEXTR for the first time will take serval minutes to
> complete as it needs to download the DEXTR docker image. Do not exit out of
> your agent unless it specifically throws an error.

## Action

### Inputs

| Name           |  Type  |         Default          | Description                                                                                                                                                                            |
| -------------- | :----: | :----------------------: | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `imagePath`    | string |        _required_        | Absolute path to image. This path must be in the agent directory.                                                                                                                      |
| `points`       | array  |        _required_        | 4 points marking the most left, right, bottom and top points of the shape.                                                                                                             |
| `url`          | string | `http://localhost:3445`  | Url for sending requests. A DEXTR docker image will be spun up on this port if not found.                                                                                              |
| `image`        | string | `datatorch/action-dextr` | Docker image to spin up.                                                                                                                                                               |
| `annotationId` | string |          `null`          | Annotation to insert segmentation into. If not provided the segmentation will not be inserted.                                                                                         |
| `simplify`     | float  |          `1.5`           | Simplification tolerance applied to segmentation before importing. Set to 0 to disable. Disabling can significantly increase pipeline performance, but decrease annotator performance. |

### Outputs

| Name           | Type  | Description                                |
| -------------- | :---: | ------------------------------------------ |
| `segmentation` | array | Segmentation of points predicted by DEXTR. |

## User Guide

This guide is intended to help first-time users setup Deep Extreme Cut
[DEXTR](https://github.com/scaelles/DEXTR-PyTorch) for usage in the Datatorch
annotator.

This guide assumes that you have already set up a project, labels, and file
sources.

### Prerequisites

- A UNIX distro (OSX, Linux, WSL, etc)
- Python 3.6+
- Docker

### Agent Setup

#### Creating Agent

First, you will need an API access key associated with your account. If you have
not generated one already, navigate to your [API Access
Keys](https://datatorch.io/settings/access-tokens) and generate a new key. Any
name will suffice. Write or copy down this key before closing out of the modal;
you will **NOT** be able to view it again.

Now open up a terminal and run the command:

`pip install datatorch[agent]`

_use `pip3` if `pip` is aliased to a 2.x version_

This should download and install the program that will create agents to run our
pipelines.

Next, run the command:

`datatorch login API_KEY`

Replace the `API_KEY` with the key that was copied earlier. The console will
display a success message alongside the username associated with the key.

Next, you will need to create and name an agent with the command:

`datatorch agent create`

You will need to run the agent itself using the command:

`datatorch agent start`

The agent will then connect with DataTorch's servers. You can confirm success by
navigating to your [agents page](https://datatorch.io/agents) and clicking on
the agent in the sidebar.

Success should look like this in the console:

```
2020-11-20 10:59:34,539 datatorch.agent                DEBUG    API Endpoint at https://datatorch.io/api
2020-11-20 10:59:34,986 datatorch.agent.agent          DEBUG    Switch to agent directory: /home/datatorch/.config/datatorch/agent
2020-11-20 10:59:34,986 datatorch.agent                DEBUG    Agent logger has been initialized.
2020-11-20 10:59:34,986 datatorch.agent.agent          INFO     Waiting for jobs.
2020-11-20 10:59:34,990 datatorch.agent.monitoring     INFO     Sending initial system metrics.
2020-11-20 10:59:36,921 datatorch.agent.monitoring     INFO     Starting system monitoring task.
2020-11-20 10:59:36,921 datatorch.agent.monitoring     DEBUG    Sampling system stats every 60 seconds.
2020-11-20 10:59:36,922 datatorch.agent.monitoring     DEBUG    System stats: CPU: 0.0, Memory: 5.5, Disk: 2.4
```

and look like this on the web client:

<p align="center">
  <img src="/images/agent_success.png" alt="Agent success shown in the agent section of user settings" align="center" height=auto/>
</p>

#### Adding Agent to Project

Although the agent is now connected to your account, the agent needs to be
attached to a specific project. On the Datatorch website, from the target
project's summary page, navigate to the project's **Settings** and click on the
**Agents** under **Pipeline**.

From here, click on the button that says **Manage Agent** and select the agent
you just created.

### Pipeline Setup

After the agent is setup, now we have to define the pipeline that will allow us
to run DEXTR. From the project page, navgiate to the **Pipelines** section under
**Workspace** in the sidebar. Click on the green plus sign to create a new
pipeline.

You'll see a default pipeline. Erase everything except for the project field
above and copy the following text into the box below the project field:

```yaml
name: DEXTR

triggers:
  annotatorButton:
    name: "DEXTR"
    icon: brain
    flow: 4-points

jobs:
  predict:
    steps:
      - name: Download File
        action: datatorch/download-file@v1
        inputs:
          fileId: ${{ event.fileId }}

      - name: Predict Segmentation
        action: datatorch/dextr@latest
        inputs:
          imagePath: ${{ input.path }}
          points: ${{ event.flowData.points }}
          annotationId: ${{ event.annotationId }}
```

Save the pipeline. If everything has been setup correctly, you should be ready
to start annotating using DEXTR!

If you are making multiple pipelines, please ensure that the top-level name
field is unique for each new pipeline.

### Usage

If the pipeline has been setup correctly, a new tool with a brain icon should
appear in the annotator:


<p align="center">
  <img src="/images/tool_appears.png" alt="Agent success shown in the agent section of user settings" align="center" height=auto/>
</p>

You can proceed to create DEXTR annotations by clicking on the icon, selecting
an appropriate label, and then creating a bounding box with four points/clicks
that encompass the object to be segmented. A loading indicator will show on the
created or edited annotation indicating that the image is being processed by the
agent.

> **NOTE:** agents running DEXTR for the first time must perform a
> download of a few gigabytes, which will take some time to complete. Your first
> annotation will take several minutes to complete. Do not exit out of your agent
> unless it specifically throws an error

Although the agent will take some time to start, as long as it is connected, you
are free to continue to make DEXTR bounding boxes and new annotations on other
objects and on other files.

<p align="center">
  <img src="/images/loading.gif" alt="DEXTR annotation is loading" align="center" height=auto/>
</p>

Once the first-time setup completes, all bounding boxes will be populated with
their DEXTR segementations. Subsequent DEXTR annotations will update a few
seconds after completing a bounding box.

<p align="center">
  <img src="/images/action.gif" alt="DEXTR tool demonstration, clicking four times" align="center" height=auto/>
</p>

Currently, re-doing DEXTR segmentations on a bounding box is not supported, but
editing existing DEXTR segmentations is supported through use of the brush and
eraser tool.

## FAQ

### Quick Debug Checklist

Have you made sure that you:

- Are working with a Python version 3.6+ and above? You can confirm your version
  with `python --version` (or `python3`).
- Have connected your agent both to your account and to the target project?
- Have verified that your agent is running? It will occasionally send system
  statistics if it is running smoothly.
- Have waited for the agent to download and setup the DEXTR action? The download
  is a few gigabytes and may take some time on first-time setup. If the agent
  seems silent, then it is still setting up.
