console.log('graphSteamUserFriendship.js loaded')
/**
 * Library shortcuts for easier access
 */
var FA2Layout = graphologyLibrary.FA2Layout;
var forceAtlas2 = graphologyLibrary.layoutForceAtlas2;
var circular = graphologyLibrary.layout.circular;
var circlepack = graphologyLibrary.layout.circlepack;
var random = graphologyLibrary.layout.random;

/**
 * 
 * Graph Init
 * 
 */
/* Container */
var container = document.getElementById("graph-canvas")
if (container == null) console.error('Cannot find canvas #graph-canvas')
/* Graph */
var graph = new graphology.Graph();
/* State Management */
var visualState = {
    graphNodeColor: "",
    graphNodeSize: "",
}

/** 
 * Get Nodes 
 **/
var steam_users_json = document.getElementById('steam_users');
if (steam_users_json == null) console.error('Cannot find <script id="steam_users" type="application/json">');
var steam_users = JSON.parse(steam_users_json.textContent);
/** 
 * Get Edges
 **/
var friendships_json = document.getElementById('steam_users_friendships');
if (friendships_json == null) console.error('Cannot find <script id="steam_users_friendships" type="application/json">');
var friendships = JSON.parse(friendships_json.textContent);

/** 
 * Add Nodes 
 **/
console.log('Start adding nodes')
for (user of steam_users) {
    graph.addNode(user.id, user);
}
console.log('End adding nodes');
/** 
 * Add Edges 
 **/
console.log('Start adding edges')
for (fs of friendships) {
    try {
        graph.addEdge(fs.source, fs.target);
    } catch (error) {
        if (error.name == 'UsageGraphError') {
        } else {
            console.error(error);
        }
    }
}
console.log('End adding edges');

// Set graph to Undirected. We don't need directions on steam user friend graph
graph = graphologyLibrary.operators.toUndirected(graph);

/**
 * 
 * Communities
 * 
 **/
communityDetails = graphologyLibrary.communitiesLouvain.detailed(graph);
console.log('communityDetails');
console.log(communityDetails);

graphologyLibrary.communitiesLouvain.assign(graph);

var communities = communityDetails.communities;
console.log('communities');
console.log(communities);

console.log('communities values');
console.log(Object.values(communities));

var communityValues = Object.values(communities);

function getUniqueVal(value, index, self) {
    return self.indexOf(value) === index;
}

var uniqueCommunities = communityValues.filter(getUniqueVal);
console.log('uniqueCommunities');
console.log(uniqueCommunities);

/* Community Count */
var communityMemberCount = {};
// Add community ids as keys
for (c of uniqueCommunities) {
    communityMemberCount[c] = 0;
}
// Add member count as values
for (c of communityValues) {
    communityMemberCount[c]++;
}
console.log('communityMemberCount:')
console.log(communityMemberCount);
/**
 * 
 * Only add color to communities with count > 1
 * 
 */
var communitiesToColor = []
for (const key in communityMemberCount) {
    if (communityMemberCount[key] > 1) {
        communitiesToColor.push(key)
    }
}
console.log(`colorCommunitiesCount:`)
console.log(communitiesToColor)

/**
 * 
 * 
 * Primary Clan
 * 
 * 
**/
var primaryClans = {};
// console.log('primaryClans')
graph.forEachNode((node, atts) => {
    if (node < 20) {
        // console.log(`${node}:`)
        // console.log(atts)
    }
    if (!primaryClans.hasOwnProperty(atts.primaryclanid)) {
        primaryClans[atts.primaryclanid] = {};
        primaryClans[atts.primaryclanid]['id'] = atts.primaryclanid;
        primaryClans[atts.primaryclanid]['count'] = 0;
        primaryClans[atts.primaryclanid]['color'] = "";
    }
    primaryClans[atts.primaryclanid]['count'] += 1;
});
// console.log('primaryClans');
// console.log(primaryClans);


/**
 * 
 * 
 * COLORS   
 * 
 * 
 */

// Cubehelix
// colors = chroma.cubehelix().scale().correctLightness().colors(communitiesToColor.length)

// paired 12
// colors = ["#a6cee3", "#1f78b4", "#b2df8a", "#33a02c", "#fb9a99", "#e31a1c", "#fdbf6f", "#ff7f00", "#cab2d6", "#6a3d9a", "#ffff99", "#b15928"]

// paired 12 - better sorted
colors = ["#1f78b4","#33a02c","#e31a1c","#ff7f00","#6a3d9a","#b15928","#a6cee3","#b2df8a","#fb9a99","#fdbf6f","#cab2d6","#ffff99",]

// set 3
//colors = ["#8dd3c7","#ffffb3","#bebada","#fb8072","#80b1d3","#fdb462","#b3de69","#fccde5","#d9d9d9","#bc80bd","#ccebc5","#ffed6f"]

console.log('colors');
console.log(colors);


/**
 * 
 * Community Colors
 * 
 */
var communityPaletteDict = {}
for (let i = 0; i < communitiesToColor.length; i++) {
    communityPaletteDict[communitiesToColor[i]] = colors[i];
}
console.log('communityPaletteDict');
console.log(communityPaletteDict);
// Add to HTML page
var communityPaletteHTML = document.getElementById('communityColorPalette')
if (communityPaletteHTML == null){
    console.error('Add #communityColorPalette to show palette on page')
} else {
    for (color of colors) {
        communityPaletteHTML.innerHTML += `<span style="background-color: ${color}; border-radius: 5px; display:inline-block; width: 20px; height: 20px;"></span>&nbsp;`
    }
}


/**
 * 
 * 
 * DEFAULT NODE SETTINGS
 * 
 * 
 */
graphologyLibrary.layout.circlepack.assign(graph, {
    hierarchyAttributes: ['degree', 'community'],
});

setNodeSizeSmall()
setNodeColorCommunity()
setEdgeColor()

var renderer = new Sigma(graph, container);
//fa2Layout.start()


/**
 * 
 * 
 * NODES TO HTML TABLE
 * 
 * 
 */
var nodeTable = document.getElementById('nodeTable');
if (nodeTable == null){
    console.error('Add #nodeTable to see a node table on page')
} else {
    graph.forEachNode((node, atts) => {
        var text = ""
        text += `<td>${atts.id}</td>`
        text += `<td>${atts.label}</td>`
        text += `<td style="background-color:${atts.color};">${atts.color}</td>`
        text += `<td>${atts.size}</td>`
        text += `<td style="background-color:${atts.color};">${atts.community}</td>`
        text += `<td>${atts.primaryclanid}</td>`
        text += `<td>${atts}</td>`
        nodeTable.innerHTML += `<tr>${text}</tr>`
    });
}


/**
 * 
 * 
 * Label Renderer
 * 
 *  
 **/
const labelsThresholdRange = document.getElementById("labels-threshold");
// Bind labels threshold to range input
labelsThresholdRange.addEventListener("input", () => {
    renderer.setSetting("labelRenderedSizeThreshold", +labelsThresholdRange.value);
});
// Set proper range initial value:
labelsThresholdRange.value = renderer.getSetting("labelRenderedSizeThreshold") + "";


/**
 * 
 * Change Node Appearance
 * 
 */
function setNodeColorCommunity() {
    console.log('set color community')
    graph.forEachNode((node, atts) => {
        // Only color node if node.community is in color dict.
        if (Object.keys(communityPaletteDict).indexOf(atts.community.toString()) > -1) {
            atts.color = communityPaletteDict[atts.community];
        }
    })
    graphNodeColor = 'COMMUNITY';
}
function setNodeSizeSmall() {
    console.log('set size small')
    graph.forEachNode((node, atts) => {
        atts.size = Math.sqrt(graph.degree(node));
    })
    graphNodeSize = 'SMALL';
}
function setNodeSizeMedium() {
    console.log('set size medium')
    graph.forEachNode((node, atts) => {
        atts.size = graph.degree(node) / 3;
    })
    graphNodeSize = 'MEDIUM';
}
function setEdgeColor() {
    // if both nodes have the same color, set edge to same color
    // Using the callback methods
    graph.forEachEdge(
        (edge, attributes, source, target, sourceAttributes, targetAttributes) => {
            if (sourceAttributes.color == targetAttributes.color) {
                console.log(`Colors are the same, setting edge color.`)
                graph.setEdgeAttribute(edge, 'color', sourceAttributes.color);
            }
        });
}


/**
 * 
 * 
 * Layout: Force Atlas 2
 * 
 * 
 */
// Buttons
const FA2Button = document.getElementById("forceatlas2")
const FA2StopLabel = document.getElementById("forceatlas2-stop-label")
const FA2StartLabel = document.getElementById("forceatlas2-start-label")
// Force Atlas 2 Init
const sensibleSettings = forceAtlas2.inferSettings(graph)
var fa2Layout = new FA2Layout(graph, {
    settings: sensibleSettings
});
// Force Atlas Control Functions
function stopFA2() {
    fa2Layout.stop()
    FA2StartLabel.style.display = "flex"
    FA2StopLabel.style.display = "none"
}
function startFA2() {
    if (graphNodeColor != 'COMMUNITY') colorNodesByCommunity()
    if (graphNodeSize != 'SMALL') setNodeSizeSmall()
    if (cancelCurrentAnimation) cancelCurrentAnimation()
    fa2Layout.start()
    FA2StartLabel.style.display = "none"
    FA2StopLabel.style.display = "flex"
}
// the main toggle function
function toggleFA2Layout() {
    if (fa2Layout.isRunning()) {
        stopFA2()
    } else {
        startFA2()
    }
}
// bind method to the forceatlas2 button
FA2Button.addEventListener("click", toggleFA2Layout)


/**
 * 
 * 
 * Random Layout
 * 
 * 
 */
// Button
const randomButton = document.getElementById("random")
// Function
function randomLayout() {
    // stop fa2 if running
    if (fa2Layout.isRunning()) stopFA2()
    random.assign(graph);
}
// Bind function to button
randomButton.addEventListener("click", randomLayout)


/**
 * 
 * 
 * Circular Layout
 * 
 * 
 */
const circularButton = document.getElementById("circular")
function circularLayout() {
    // stop fa2 if running
    if (fa2Layout.isRunning()) stopFA2()
    circular.assign(graph, { scale: 100 });
}
// bind method to the random button
circularButton.addEventListener("click", circularLayout)


/**
 * 
 * 
 * Circle Pack Layout (Default Circle Pack = Community)
 * 
 * 
 */
// Button
const circlepackButton = document.getElementById("circlepack")
// Function
function circlepackLayout() {
    // stop fa2 if running
    if (fa2Layout.isRunning()) stopFA2()
    if (graphNodeSize != 'SMALL') setNodeSizeSmall()
    if (graphNodeColor != 'COMMUNITY') setNodeColorCommunity()
    circlepack.assign(graph, { scale: 100, hierarchyAttributes: ['degree', 'community'], });
}
// Bind function to button
circlepackButton.addEventListener("click", circlepackLayout)


/**
 * 
 * 
 * CIRCLE PACK PRIMARYCLAN LAYOUT 
 * 
 * 
 */
const circlepackPrimaryClanButton = document.getElementById("circlepackPrimaryClan")
function circlepackPrimaryClanLayout() {
    // stop fa2 if running
    if (fa2Layout.isRunning()) stopFA2()
    if (cancelCurrentAnimation) cancelCurrentAnimation()

    circlepack.assign(graph, { scale: 100, hierarchyAttributes: ['primaryclanid'], });
}
// bind method to the random button
circlepackPrimaryClanButton.addEventListener("click", circlepackPrimaryClanLayout)
