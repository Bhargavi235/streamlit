import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import time

# We use this to keep track of which buildings are connected.
class UnionFind:
    # Initialize the Disjoint Set for all buildings.
    def __init__(self, vertices):
        # Set each building to be its own parent initially.
        self.parent = {v: v for v in vertices}
        # Set the initial rank (tree height) of each building to 0.
        self.rank = {v: 0 for v in vertices}

    # Find the root leader of the set that 'item' belongs to.
    def find(self, item):
        # Check if the building is its own parent.
        if self.parent[item] != item:
            # If not, recursively find the root, and point the current building directly to the root (Path Compression).
            self.parent[item] = self.find(self.parent[item])
        # Return the root building of the set.
        return self.parent[item]

    # Connect two sets of buildings together.
    def union(self, set1, set2):
        # Find the root leader of the first building.
        root1 = self.find(set1)
        # Find the root leader of the second building.
        root2 = self.find(set2)

        # Ensure they are not already in the same set to avoid cycles.
        if root1 != root2:
            # Connect the smaller tree under the root of the larger tree (Union by Rank).
            if self.rank[root1] > self.rank[root2]:
                # Make root1 the parent of root2.
                self.parent[root2] = root1
            elif self.rank[root1] < self.rank[root2]:
                # Make root2 the parent of root1.
                self.parent[root1] = root2
            else:
                # If both trees have the same height, pick one as parent and increase its height.
                self.parent[root2] = root1
                # Increase the rank of root1 since it gained a new level.
                self.rank[root1] += 1

# --- GRAPH DATA SETUP ---
# Define the 7 buildings in our campus.
buildings = ["Main Block", "CS Block", "Library", "Cafeteria", "Hostel", "Auditorium", "Sports Complex"]

# Define the possible network connections (edges) with illustrative installation costs in Rupees (₹).
connections = [
    ("Main Block", "CS Block", 25),
    ("Main Block", "Library", 20),
    ("CS Block", "Library", 35),
    ("CS Block", "Cafeteria", 30),
    ("Library", "Cafeteria", 15),
    ("Library", "Auditorium", 40),
    ("Cafeteria", "Hostel", 20),
    ("Cafeteria", "Sports Complex", 45),
    ("Hostel", "Sports Complex", 30),
    ("Auditorium", "Sports Complex", 25),
    ("Main Block", "Auditorium", 50)
]

# Sort all connections by cost in ascending order (Step 1 of Kruskal's Algorithm).
sorted_connections = sorted(connections, key=lambda item: item[2])

# --- STATE INITIALIZATION ---
# Initialize Streamlit session state variables to track the algorithm's progress step-by-step.
if "step" not in st.session_state:
    # Set the initial step to 0 (no edges processed yet).
    st.session_state.step = 0
if "mst_edges" not in st.session_state:
    # Create an empty list to store edges that are accepted into the Minimum Spanning Tree.
    st.session_state.mst_edges = []
if "rejected_edges" not in st.session_state:
    # Create an empty list to store edges that create a cycle and are rejected.
    st.session_state.rejected_edges = []
if "total_cost" not in st.session_state:
    # Set the initial total minimum cost to 0.
    st.session_state.total_cost = 0
if "uf" not in st.session_state:
    # Create a fresh Union-Find structure for the buildings.
    st.session_state.uf = UnionFind(buildings)
if "finished" not in st.session_state:
    # Flag to indicate if the algorithm has finished checking all edges or connected all buildings.
    st.session_state.finished = False
if "current_message" not in st.session_state:
    # Store a message explaining the action taken in the current step.
    st.session_state.current_message = ""
if "auto_run" not in st.session_state:
    # Flag to indicate if the automatic execution loop is running.
    st.session_state.auto_run = False

# --- DRAWING FUNCTION ---
# Function to visualize the campus network graph.
def draw_graph(mst, rejected, current_edge=None):
    # Create a new matplotlib figure.
    fig, ax = plt.subplots(figsize=(8, 6))
    # Create an empty NetworkX graph.
    G = nx.Graph()
    
    # Add all building nodes to the graph.
    for b in buildings:
        # Add node 'b'.
        G.add_node(b)
        
    # Add all possible connections as edges to the graph.
    for u, v, w in connections:
        # Add edge with a 'weight' attribute.
        G.add_edge(u, v, weight=w)
        
    # Generate positions for all nodes using a spring layout for better visual distribution.
    pos = nx.spring_layout(G, seed=42)
    
    # Draw all nodes with a specific color and size.
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=2500, ax=ax)
    # Draw labels for all nodes.
    nx.draw_networkx_labels(G, pos, font_size=9, font_weight="bold", ax=ax)
    
    # List to store edges that haven't been checked yet.
    pending_edges = []
    # Loop through all connections to classify them for drawing.
    for u, v, w in connections:
        # Sort the endpoints so order doesn't matter when checking presence in lists.
        edge = tuple(sorted((u, v)))
        # Format the current edge similarly if it exists.
        c_edge = tuple(sorted((current_edge[0], current_edge[1]))) if current_edge else None
        
        # Check if the edge is in the accepted MST list.
        if (u, v, w) in mst or (v, u, w) in mst:
            # Draw accepted MST edges in green and thicker.
            nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], width=3, edge_color='green', ax=ax)
        # Check if the edge is in the rejected list.
        elif (u, v, w) in rejected or (v, u, w) in rejected:
            # Draw rejected edges in red with a dashed style.
            nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], width=1, edge_color='red', style='dashed', ax=ax)
        # Check if the edge is the one currently being evaluated.
        elif edge == c_edge:
            # Draw the current edge in orange and thicker to highlight it.
            nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], width=4, edge_color='orange', ax=ax)
        else:
            # Add to pending edges if not evaluated yet.
            pending_edges.append((u, v))
            
    # Draw the pending edges in gray.
    nx.draw_networkx_edges(G, pos, edgelist=pending_edges, width=1, edge_color='gray', alpha=0.5, ax=ax)
    
    # Get edge weight labels to display on the graph.
    edge_labels = nx.get_edge_attributes(G, 'weight')
    # Prepend ₹ symbol to the edge weights.
    edge_labels_formatted = {k: f"₹{v}" for k, v in edge_labels.items()}
    # Draw the formatted edge labels on the graph.
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels_formatted, font_size=8, ax=ax)
    
    # Remove axis boundaries for a cleaner look.
    ax.axis('off')
    # Return the generated figure.
    return fig

# --- MAIN APP UI ---
# Set the title of the Streamlit application.
st.title("CampusNet")
# Add a subtitle.
st.subheader("Minimum-Cost Campus Network Planner")
# Write a brief explanation of the application's purpose.
st.write("A college wants to connect all of its campus buildings through network infrastructure. Several possible connections are available between buildings, and each connection has an illustrative installation cost. The goal is to connect every building while minimizing the total installation cost.")
# Add a disclaimer that costs are illustrative.
st.info("The connection costs are illustrative values representing the relative installation cost of connecting two buildings. Higher values can be interpreted as longer or more expensive network connections.")

# Create two columns for the UI layout.
col1, col2 = st.columns([2, 1])

# In the first column, show the graph visualization.
with col1:
    # Check if there is an edge currently being evaluated.
    current_edge_eval = sorted_connections[st.session_state.step] if st.session_state.step < len(sorted_connections) and not st.session_state.finished else None
    # Draw and display the graph using matplotlib.
    st.pyplot(draw_graph(st.session_state.mst_edges, st.session_state.rejected_edges, current_edge_eval))
    
    # Show a legend for the graph colors.
    st.markdown("**Legend:** ⚪ Unchecked | 🟠 Current | 🟢 Accepted | 🔴 Rejected (Cycle)")
    
    # If a message exists, display it.
    if st.session_state.current_message:
        # Show the message as an info box.
        st.info(st.session_state.current_message)

# In the second column, show controls and status.
with col2:
    # Add a section header for controls.
    st.write("### Controls")
    
    # Function to execute a single step of Kruskal's algorithm.
    def next_step():
        # Check if we haven't finished and there are still edges to process.
        if not st.session_state.finished and st.session_state.step < len(sorted_connections):
            # Get the next cheapest edge from the sorted list.
            u, v, cost = sorted_connections[st.session_state.step]
            
            # Find the root sets for both buildings connected by this edge.
            root_u = st.session_state.uf.find(u)
            root_v = st.session_state.uf.find(v)
            
            # Find the representative/root of each building's connected component.
            # If both buildings have the same root, they are already connected.
            # Adding this edge would therefore create a cycle.
            # If the roots are different, the edge connects two separate components and can be safely added to the MST.
            if root_u != root_v:
                # The buildings are in different sets, so no cycle is created. Accept the edge.
                st.session_state.mst_edges.append((u, v, cost))
                # Add the cost to the total MST cost.
                st.session_state.total_cost += cost
                # Union the two sets so they are now connected.
                st.session_state.uf.union(u, v)
                # Set a success message explaining the acceptance.
                st.session_state.current_message = f"### Current Edge\n{u} → {v}\n\n### Cost\n₹{cost}\n\n### Decision\n✓ ACCEPTED\n\n### Reason\nThe two buildings belong to different sets, so adding this edge does not create a cycle."
            else:
                # The buildings are in the same set, meaning there is already a path between them.
                st.session_state.rejected_edges.append((u, v, cost))
                # Set a rejection message explaining the cycle creation.
                st.session_state.current_message = f"### Current Edge\n{u} → {v}\n\n### Cost\n₹{cost}\n\n### Decision\n✗ REJECTED\n\n### Reason\nThe two buildings already belong to the same connected component, so adding this edge would create a cycle."
            
            # Increment the step counter to look at the next edge next time.
            st.session_state.step += 1
            
            # Check if we have successfully connected all V buildings (which requires V-1 edges).
            if len(st.session_state.mst_edges) == len(buildings) - 1:
                # If so, the algorithm is finished.
                st.session_state.finished = True
                # Update the message to indicate completion.
                st.session_state.current_message += "\n\n**Algorithm Finished!** All buildings are now connected."
        # If we run out of edges before connecting everything, mark as finished.
        elif st.session_state.step >= len(sorted_connections):
            # Mark finished.
            st.session_state.finished = True
            
    # Button to execute one step of the algorithm.
    if st.button("Next Step", disabled=st.session_state.finished):
        # Call the next_step function.
        next_step()
        
    # Button to automatically run the algorithm to the end.
    if st.button("Run Kruskal Automatically", disabled=st.session_state.finished):
        # Set a flag in session state to trigger automatic execution at the bottom of the script.
        st.session_state.auto_run = True
        # Force a rerun to start the automatic loop.
        st.rerun()

    # Button to instantly show the final MST result.
    if st.button("Show Final MST", disabled=st.session_state.finished):
        # Loop through all remaining edges instantly.
        while not st.session_state.finished:
            # Execute one step.
            next_step()
        # Rerun to update the final view.
        st.rerun()
            
    # Button to reset the application state.
    if st.button("Reset"):
        # Reset the step counter.
        st.session_state.step = 0
        # Clear accepted edges.
        st.session_state.mst_edges = []
        # Clear rejected edges.
        st.session_state.rejected_edges = []
        # Reset total cost to 0.
        st.session_state.total_cost = 0
        # Reinitialize Union-Find.
        st.session_state.uf = UnionFind(buildings)
        # Mark as not finished.
        st.session_state.finished = False
        # Clear the current message.
        st.session_state.current_message = ""
        # Turn off automatic execution.
        st.session_state.auto_run = False
        # Rerun to clear the UI.
        st.rerun()

    # Display a summary of the current state.
    st.write("### Status")
    # Show the number of edges currently in the MST.
    st.write(f"**Selected Edges:** {len(st.session_state.mst_edges)} / {len(buildings) - 1}")
    # Show the total cost accumulated so far.
    st.write(f"**Current Total Cost:** ₹{st.session_state.total_cost}")

# --- FINAL RESULTS SECTION ---
# Add a divider for visual separation.
st.divider()

# If the algorithm has finished connecting everything, show the final report.
if st.session_state.finished:
    # Display header for final results.
    st.write("## Final Minimum Spanning Tree")
    # Show the number of buildings.
    st.write(f"- **Buildings:** {len(buildings)}")
    # Show the total number of possible connections.
    st.write(f"- **Possible connections:** {len(connections)}")
    # Show the number of edges selected for the MST.
    st.write(f"- **Selected connections:** {len(st.session_state.mst_edges)}")
    # Display the final minimum cost prominently.
    st.write(f"- **Total minimum installation cost:** ₹{st.session_state.total_cost}")
    # Provide confirmation that all buildings are successfully connected.
    st.success("Status: All buildings connected")
    
# --- EDGE TABLE SECTION ---
# Display a header for the edge tracking table.
st.write("## Edge Evaluation Table")

# Create a simple HTML table to show the status of all evaluated edges.
table_html = "<table style='width:100%; text-align:left;'><tr><th>Connection</th><th>Cost</th><th>Status</th></tr>"

# Loop through all edges processed so far.
for i in range(st.session_state.step):
    # Retrieve the connection details.
    u, v, w = sorted_connections[i]
    # Check if the edge was accepted into the MST.
    if (u, v, w) in st.session_state.mst_edges:
        # Mark as Selected in green.
        status = "<span style='color:green;font-weight:bold;'>Selected</span>"
    else:
        # Mark as Rejected in red.
        status = "<span style='color:red;'>Rejected</span>"
    
    # Add a row to the HTML table.
    table_html += f"<tr><td>{u} – {v}</td><td>₹{w}</td><td>{status}</td></tr>"

# Close the HTML table tag.
table_html += "</table>"
# Render the HTML table in Streamlit safely.
st.markdown(table_html, unsafe_allow_html=True)

# --- EDUCATIONAL EXPLANATION SECTION ---
# Add a divider for visual separation.
st.divider()
# Header for the explanation section.
st.write("## How Kruskal's Algorithm Works")
# Write simple student-friendly explanations of the algorithm steps.
st.write("""
1. **Sort** all possible network connections (edges) by their installation cost from lowest to highest.
2. **Pick** the cheapest available connection.
3. **Check** whether adding this connection forms a loop (cycle) among the buildings.
4. **Accept** the connection if it does NOT create a cycle.
5. **Reject** the connection if it DOES create a cycle.
6. **Continue** this process until all buildings are connected (which requires exactly V-1 connections for V buildings).

The final resulting network is called a **Minimum Spanning Tree (MST)**.
""")

# --- COMPLEXITY SECTION ---
# Display theoretical time and space complexity.
st.write("### Theoretical Complexity")
# State Time Complexity.
st.write("**Time Complexity:** `O(E log E)`")
# Explain why Time Complexity is O(E log E).
st.write("The dominant operation is sorting the edges based on their cost. The Union-Find operations take nearly `O(1)` time.")
# State Space Complexity.
st.write("**Space Complexity:** `O(V + E)`")
# Explain Space Complexity.
st.write("Required to store the graph structures and the Union-Find parent/rank arrays.")

# --- TESTING FUNCTIONALITY ---
# A simple internal test to verify algorithm correctness logic.
def test_kruskal():
    # Instantiate Union-Find for testing.
    uf_test = UnionFind(buildings)
    # Track accepted test edges.
    mst_test = []
    # Track total cost.
    cost_test = 0
    # Simulate Kruskal's logic.
    for u, v, w in sorted_connections:
        # If they are in different sets...
        if uf_test.find(u) != uf_test.find(v):
            # Union the sets.
            uf_test.union(u, v)
            # Add to test MST.
            mst_test.append((u, v, w))
            # Add to cost.
            cost_test += w
            
    # Verify we selected exactly V-1 edges.
    assert len(mst_test) == len(buildings) - 1, "MST should have V-1 edges"
    # Verify the total cost matches the expected ₹135 for this specific demo graph.
    assert cost_test == 135, f"Expected cost 135, but got {cost_test}"
    # Verify all buildings are connected (all have the same root).
    root_first = uf_test.find(buildings[0])
    # Check each remaining building.
    for b in buildings[1:]:
        assert uf_test.find(b) == root_first, f"Building {b} is not connected to the main component."
    
    # Return True if logic matches expected results.
    return True

# Call test silently, just to ensure logic holds up in the background.
# (If it fails, it will raise an AssertionError in the console, ensuring correctness during runtime).
test_kruskal()

# --- AUTOMATIC EXECUTION LOOP ---
# If auto_run flag is set and we haven't finished the algorithm yet.
if st.session_state.get('auto_run', False) and not st.session_state.finished:
    # Add a small delay so the user can see the algorithm progress.
    time.sleep(1.0)
    # Execute the next step.
    next_step()
    # Rerun the script to update the visuals and trigger the next loop iteration.
    st.rerun()
# If auto_run flag is set but we are finished, turn off the flag.
elif st.session_state.get('auto_run', False) and st.session_state.finished:
    # Disable the automatic execution flag.
    st.session_state.auto_run = False
