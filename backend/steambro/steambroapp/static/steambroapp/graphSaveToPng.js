
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
const loadImage = path => {
    return new Promise((resolve, reject) => {
        const img = new Image()
        img.crossOrigin = 'Anonymous' // to avoid CORS if used with Canvas
        img.src = path
        img.onload = () => {
            resolve(img)
        }
        img.onerror = e => {
            reject(e)
        }
    })
}

async function saveAsPNG(renderer, inputLayers) {
    // const { width, height } = renderer.getDimensions()
    const width = 1500
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
    /*
    console.log('Removing nodes with degree = 0');
    renderer.getGraph().forEachNode((node, attributes) => {
        var degree = renderer.getGraph().degree(node)
        if (degree == 0){
            renderer.getGraph().dropNode(node);
        }
        attributes.label = `${attributes.personaname}(${degree})`
    });
    */

    /* Rename Nodes */
    console.log('Rename Nodes');
    renderer.getGraph().forEachNode((node, attributes) => {
        // var degree = renderer.getGraph().degree(node)
        attributes.label = `${attributes.personaname}`
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
    })
    tmpRenderer.refresh()

    // Create a new canvas, on which the different layers will be drawn:
    const canvas = document.createElement("CANVAS")
    canvas.setAttribute("width", width * pixelRatio + "")
    canvas.setAttribute("height", height * pixelRatio + "")
    const ctx = canvas.getContext("2d")

    // draw a rounded rectangle with background
    const roundRect = (info, radius = { tr: 4, br: 4, bl: 4, tl: 4 }, color = '#ffffff') => {
        const { x, y, w, h } = info;
        const r = x + w;
        const b = y + h;
        ctx.beginPath();
        ctx.fillStyle = color;
        ctx.moveTo(x + radius.tl, y);
        ctx.lineTo(r - radius.tr, y);
        ctx.quadraticCurveTo(r, y, r, y + radius.tr);
        ctx.lineTo(r, y + h - radius.br);
        ctx.quadraticCurveTo(r, b, r - radius.br, b);
        ctx.lineTo(x + radius.bl, b);
        ctx.quadraticCurveTo(x, b, x, b - radius.bl);
        ctx.lineTo(x, y + radius.tl);
        ctx.quadraticCurveTo(x, y, x + radius.tl, y);
        ctx.stroke();
        ctx.fill();
        ctx.closePath();
    }

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

    // Add Background To Text
    /*
    const r1Info = { x: 25, y: height-25-128-64, w: 650, h: 200 };
    const r1Radius = { tr: 5, br: 40, bl: 5, tl: 20 };
    roundRect(r1Info, r1Radius, chroma('#1f78b4').brighten().desaturate().alpha(0.5));
    */

    // Add text to image
    var watermark = JSON.parse(document.getElementById('watermark').textContent);
    console.log('watermark');
    console.log(watermark);
    ctx.fillStyle = chroma('#1f78b4')
    if (watermark != null) {
        console.log('Writing on canvas')


        // WAIT TILL IMAGE IS LOADED.
        ctx.font = '24px serif';
        ctx.fillText('Friend Network For', 50, height - 50 - (24 * 2) - 64 - 4);

        // Image
        const img = await loadImage(watermark.avatar);
        console.log('img loaded')
        ctx.drawImage(img, 50, height - 50 - (24 * 2) - 64);       // DRAW THE IMAGE TO THE CANVAS.

        // Either SteamGroup or SteamUser
        ctx.font = 'bold 64px serif';
        ctx.fillText(`${watermark.name}`, 50 + 64 + 8, height - 50 - (24 * 2) - 4);

        ctx.font = '24px serif';
        // Url to SteamUser of SteamGroup
        ctx.fillText(`${watermark.steamurl}`, 50, height - 50 - 24);
    }
    ctx.font = '24px serif';
    ctx.fillText('Render by https://steambro.party', 50, height - 50);


    // Save the canvas as a PNG image:
    var filename = "graph.png"
    if (watermark.name != null) {
        filename = watermark.name
    }
    canvas.toBlob(blob => {
        if (blob) saveAs(blob, filename)

        // Cleanup:
        tmpRenderer.kill()
        tmpRoot.remove()
    }, "image/png")
}


// Bind save button:
const saveBtn = document.getElementById("save-as-png");
if (saveBtn == null) {
    console.warn('Let user save graph to png, add: #save-as-png')
} else {
    saveBtn.addEventListener("click", () => {
        const layers = ["edges", "nodes", "edgeLabels", "labels"];
        saveAsPNG(renderer, layers);
    });
}