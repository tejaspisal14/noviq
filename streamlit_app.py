import streamlit as st
from src.search import search_patents
from src.analyzer import analyze_novelty
import plotly.graph_objects as go
import networkx as nx

st.set_page_config(
    page_title="Noviq",
    page_icon="N",
    layout="wide"
)

st.markdown("""
<style>

.stApp {
    background-color: #050816;
}

.main-title {
    text-align: center;
    font-size: 80px;
    font-weight: 800;
    color: white;
    letter-spacing: 4px;
    margin-bottom: 0px;
}

.sub-title {
    text-align: center;
    color: #A0AEC0;
    font-size: 24px;
    margin-top: -20px;
}

.tagline {
    text-align: center;
    color: #718096;
    font-size: 16px;
    margin-bottom: 40px;
}

</style>
""", unsafe_allow_html=True)

st.markdown(
    '<p class="main-title">NOVIQ</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="sub-title">Innovation Intelligence Platform</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="tagline">Assess novelty • Discover prior art • Evaluate patentability</p>',
    unsafe_allow_html=True
)

idea = st.text_area(
    "Describe your invention",
    height=120,
    placeholder="Example: AI-powered highway safety network that predicts animal crossings using thermal cameras, migration history, and weather data"
)

analyze = st.button(
    "Analyze Innovation",
    use_container_width=True
)

if analyze and idea:

    progress = st.progress(
        0,
        text="Building semantic embeddings..."
    )

    progress.progress(
        25,
        text="Searching patent database..."
    )

    patents = search_patents(idea)

    progress.progress(
        75,
        text="Generating novelty assessment..."
    )

    analysis = analyze_novelty(
        idea,
        patents
    )

    progress.progress(
        100,
        text="Analysis complete"
    )

    # --------------------------
    # Dynamic novelty score
    # --------------------------

    similarities = []

    for patent in patents:

        similarity = max(
            0,
            min(
                100,
                100 - patent["distance"]
            )
        )

        similarities.append(similarity)

    avg_similarity = (
        sum(similarities) / len(similarities)
        if similarities
        else 50
    )

    novelty_score = int(
        max(
            5,
            100 - avg_similarity
        )
    )

    if novelty_score >= 75:
        risk_level = "Low"

    elif novelty_score >= 45:
        risk_level = "Medium"

    else:
        risk_level = "High"

    st.divider()

    # --------------------------
    # Novelty Gauge
    # --------------------------

    gauge_fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=novelty_score,
            title={"text": "Novelty Score"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#00D4FF"}
            }
        )
    )

    gauge_fig.update_layout(
        paper_bgcolor="#050816",
        font_color="white"
    )

    st.plotly_chart(
        gauge_fig,
        use_container_width=True
    )

    st.divider()

    left, right = st.columns([3, 1])

    with left:

        st.header("Top Similar Patents")

        for patent in patents:

            similarity = max(
                0,
                100 - patent["distance"]
            )

            with st.expander(
                f"{patent['title']} • {similarity:.2f}% Match"
            ):

                st.write("### Abstract")

                st.write(
                    patent["abstract"]
                )

    with right:

        st.metric(
            "Novelty Score",
            novelty_score
        )

        st.metric(
            "Risk Level",
            risk_level
        )

        st.metric(
            "Patents Found",
            len(patents)
        )

        st.progress(
            novelty_score
        )

    st.divider()

    # --------------------------
    # Patent Landscape
    # --------------------------

    st.subheader(
        "Patent Landscape"
    )

    G = nx.Graph()

    G.add_node(
        "Your Idea"
    )

    for patent in patents:

        G.add_node(
            patent["title"]
        )

        G.add_edge(
            "Your Idea",
            patent["title"]
        )

    pos = nx.spring_layout(
        G,
        seed=42
    )

    edge_x = []
    edge_y = []

    for edge in G.edges():

        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]

        edge_x.extend(
            [x0, x1, None]
        )

        edge_y.extend(
            [y0, y1, None]
        )

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        mode="lines",
        line=dict(
            width=2,
            color="#00D4FF"
        ),
        hoverinfo="none"
    )

    node_x = []
    node_y = []
    node_text = []

    for node in G.nodes():

        x, y = pos[node]

        node_x.append(x)
        node_y.append(y)
        node_text.append(node)

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers+text",
        text=node_text,
        textposition="top center",
        marker=dict(
            size=28,
            color="#00D4FF"
        )
    )

    graph_fig = go.Figure(
        data=[
            edge_trace,
            node_trace
        ]
    )

    graph_fig.update_layout(
        showlegend=False,
        paper_bgcolor="#050816",
        plot_bgcolor="#050816",
        font_color="white",
        xaxis=dict(
            visible=False
        ),
        yaxis=dict(
            visible=False
        )
    )

    st.plotly_chart(
        graph_fig,
        use_container_width=True
    )

    st.divider()

    # --------------------------
    # AI Analysis
    # --------------------------

    st.header(
        "NOVIQ Analysis"
    )

    st.markdown(
        analysis
    )