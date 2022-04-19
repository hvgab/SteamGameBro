
    /**
    * There is a bug I can't find sources about, that makes it impossible to render
    * WebGL canvases using `#drawImage` as long as they appear onscreen. There are
    * basically two solutions:
    * 1. Use `webGLContext#readPixels`, transform it to an ImageData, put that
    *    ImageData in another canvas, and draw this canvas properly using
    *    `#drawImage`
    * 2. Hide the sigma instance
    * 3. Create a new sigma instance similar to the initial one (dimensions,
    *    settings, graph, camera...), use it and kill it
    * This exemple uses this last solution.
    */
   console.log('Adding save-to-png module')
    async function saveAsPNG(renderer, inputLayers) {
    // const { width, height } = renderer.getDimensions()
    const width = 1920
    const height = width

    // This pixel ratio is here to deal with retina displays.
    // Indeed, for dimensions W and H, on a retina display, the canvases
    // dimensions actually are 2 * W and 2 * H. Sigma properly deals with it, but
    // we need to readapt here:
    const pixelRatio = window.devicePixelRatio || 1

    const tmpRoot = document.createElement("DIV")
    tmpRoot.style.width = `${width}px`
    tmpRoot.style.height = `${height}px`
    tmpRoot.style.position = "absolute"
    tmpRoot.style.right = "101%"
    tmpRoot.style.bottom = "101%"
    document.body.appendChild(tmpRoot)

    // remove single nodes from atlas view
    console.log('Removing nodes with degree = 0');
    renderer.getGraph().forEachNode((node, attributes) => {
        var degree = renderer.getGraph().degree(node)
        if (degree == 0){
            renderer.getGraph().dropNode(node);
        }
        attributes.label = `${attributes.personaname}(${degree})`
    });

    // Instantiate sigma:
    const tmpRenderer = new Sigma(
        renderer.getGraph(),
        tmpRoot,
        renderer.getSettings()
    )


    // Copy camera and force to render now, to avoid having to wait the schedule /
    // debounce frame:
    // tmpRenderer.getCamera().setState(renderer.getCamera().getState())  // same as you view
    tmpRenderer.getCamera().setState({
        x: 0.5,
        y: 0.5,
        ratio: 1,
        angle: 0,
      },)
    tmpRenderer.refresh()

    // Create a new canvas, on which the different layers will be drawn:
    const canvas = document.createElement("CANVAS")
    canvas.setAttribute("width", width * pixelRatio + "")
    canvas.setAttribute("height", height * pixelRatio + "")
    const ctx = canvas.getContext("2d")

    // Draw a white background first:
    ctx.fillStyle = "#fff"
    ctx.fillRect(0, 0, width * pixelRatio, height * pixelRatio)

    // For each layer, draw it on our canvas:
    const canvases = tmpRenderer.getCanvases()
    const layers = inputLayers
        ? inputLayers.filter(id => !!canvases[id])
        : Object.keys(canvases)
    layers.forEach(id => {
        ctx.drawImage(
        canvases[id],
        0,
        0,
        width * pixelRatio,
        height * pixelRatio,
        0,
        0,
        width * pixelRatio,
        height * pixelRatio
        )
    })

    // Save the canvas as a PNG image:
    canvas.toBlob(blob => {
        if (blob) saveAs(blob, "graph.png")

        // Cleanup:
        tmpRenderer.kill()
        tmpRoot.remove()
    }, "image/png")
    }


    // Bind save button:
    const saveBtn = document.getElementById("save-as-png");
    saveBtn.addEventListener("click", () => {
    const layers = ["edges", "nodes", "edgeLabels", "labels"];
    saveAsPNG(renderer, layers);
    });