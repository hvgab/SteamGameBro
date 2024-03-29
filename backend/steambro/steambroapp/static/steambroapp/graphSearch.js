
console.log('ADDING SEARCH')




    /* Search button */
    const searchInput = document.getElementById("search-input");
    const searchSuggestions = document.getElementById("suggestions");
    
    const state = { searchQuery: "" }
    // Feed the datalist autocomplete values:
    searchSuggestions.innerHTML = graph.nodes().map(
        node => `<option value="${graph.getNodeAttribute(node, "label")}"></option>`
    )
        .join("\n")



    // Actions:
function setSearchQuery(query) {
    state.searchQuery = query

    if (searchInput.value !== query) searchInput.value = query

    if (query) {
        const lcQuery = query.toLowerCase()
        const suggestions = graph
            .nodes()
            .map(n => ({ id: n, label: graph.getNodeAttribute(n, "label") }))
            .filter(({ label }) => label.toLowerCase().includes(lcQuery))

        // If we have a single perfect match, them we remove the suggestions, and
        // we consider the user has selected a node through the datalist
        // autocomplete:
        if (suggestions.length === 1 && suggestions[0].label === query) {
            state.selectedNode = suggestions[0].id
            state.suggestions = undefined

            // Move the camera to center it on the selected node:
            const nodePosition = renderer.getNodeDisplayData(state.selectedNode)
            renderer.getCamera().animate(nodePosition, {
                duration: 500
            })
        }
        // Else, we display the suggestions list:
        else {
            state.selectedNode = undefined
            state.suggestions = new Set(suggestions.map(({ id }) => id))
        }
    }
    // If the query is empty, then we reset the selectedNode / suggestions state:
    else {
        state.selectedNode = undefined
        state.suggestions = undefined
    }

    // Refresh rendering:
    renderer.refresh()
}
function setHoveredNode(node) {
    if (node) {
        state.hoveredNode = node
        state.hoveredNeighbors = new Set(graph.neighbors(node))
    } else {
        state.hoveredNode = undefined
        state.hoveredNeighbors = undefined
    }

    // Refresh rendering:
    renderer.refresh()
}

// Bind search input interactions:
searchInput.addEventListener("input", () => {
    setSearchQuery(searchInput.value || "")
})
searchInput.addEventListener("blur", () => {
    setSearchQuery("")
})

// Bind graph interactions:
renderer.on("enterNode", ({ node }) => {
    setHoveredNode(node)
})
renderer.on("leaveNode", () => {
    setHoveredNode(undefined)
})

// Render nodes accordingly to the internal state:
// 1. If a node is selected, it is highlighted
// 2. If there is query, all non-matching nodes are greyed
// 3. If there is a hovered node, all non-neighbor nodes are greyed
renderer.setSetting("nodeReducer", (node, data) => {
    const res = { ...data }

    if (
        state.hoveredNeighbors &&
        !state.hoveredNeighbors.has(node) &&
        state.hoveredNode !== node
    ) {
        res.label = ""
        res.color = "#f6f6f6"
    }

    if (state.selectedNode === node) {
        res.highlighted = true
    } else if (state.suggestions && !state.suggestions.has(node)) {
        res.label = ""
        res.color = "#f6f6f6"
    }

    return res
})

// Render edges accordingly to the internal state:
// 1. If a node is hovered, the edge is hidden if it is not connected to the
//    node
// 2. If there is a query, the edge is only visible if it connects two
//    suggestions
renderer.setSetting("edgeReducer", (edge, data) => {
    const res = { ...data }

    if (state.hoveredNode && !graph.hasExtremity(edge, state.hoveredNode)) {
        res.hidden = true
    }

    if (
        state.suggestions &&
        (!state.suggestions.has(graph.source(edge)) ||
            !state.suggestions.has(graph.target(edge)))
    ) {
        res.hidden = true
    }

    return res
})