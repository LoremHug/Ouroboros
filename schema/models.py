"""Pydantic models — single source of truth for graph structure."""
from __future__ import annotations
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, Field


class Status(str, Enum):
    DEMONSTRATED = "DEMONSTRATED"
    STRONG = "STRONG"
    CONDITIONAL = "CONDITIONAL"
    OPERATIONAL = "OPERATIONAL"
    SPECULATIVE = "SPECULATIVE"
    STUB = "STUB"


class Layer(str, Enum):
    CORE = "core"
    STRUCTURE = "structure"
    EPISTEMICS = "epistemics"
    OBSERVERS = "observers"
    PHYSICS = "physics"
    COMMS = "comms"
    NUMERIC = "numeric"


class Node(BaseModel):
    id: str
    title: str = ""
    layer: Layer = Layer.NUMERIC
    status: Status = Status.STUB
    anchors: int = 0
    a_infinity: bool = False
    summary: str = ""
    why_status: str = ""
    content: str = ""
    z_struct: float = 0.0
    z_therm: float = 0.0
    z_hidden: float = 0.0
    level: int = -1
    is_placeholder: bool = False
    aliases: list[str] = Field(default_factory=list)


class EdgeStatus(str, Enum):
    D = "D"
    S = "S"


class Edge(BaseModel):
    source: str
    target: str
    label: str = ""
    edge_status: EdgeStatus = EdgeStatus.D
    justification: str = ""
    why_forced: str = ""


# Layer assignment — explicit map from manifest. Anything not listed → numeric.
LAYER_MAP: dict[str, Layer] = {
    # core
    "DEF": Layer.CORE,
    "N_ForcedId": Layer.CORE,
    "N_InversiveTheory": Layer.CORE,
    "N_NoSeparatePieces": Layer.CORE,
    "N_Invariants": Layer.CORE,
    "N310": Layer.CORE,
    # structure
    "N_Triangulation": Layer.STRUCTURE,
    "N_ZGaugeDecomposition": Layer.STRUCTURE,
    "N_TopologyProcessIdentity": Layer.STRUCTURE,
    "N_Logic": Layer.STRUCTURE,
    "N_Math": Layer.STRUCTURE,
    "N_PhiAttractor": Layer.STRUCTURE,
    "N067": Layer.STRUCTURE,
    "N370": Layer.STRUCTURE,
    # epistemics
    "N_EpistemicTraps": Layer.EPISTEMICS,
    "N_GrammarTrap": Layer.EPISTEMICS,
    "N_OntologyGate": Layer.EPISTEMICS,
    "N_Ontology": Layer.EPISTEMICS,
    "N_TranslationLayer": Layer.EPISTEMICS,
    # observers
    "N_BPIEngagement": Layer.OBSERVERS,
    "N_DopaminePredictionError": Layer.OBSERVERS,
    "N_FEP": Layer.OBSERVERS,
    "N_EngagementArchitecture": Layer.OBSERVERS,
    "N188": Layer.OBSERVERS,
    "N183": Layer.OBSERVERS,  # Topology of Cognitive States — neurosis/meditation
    "N187": Layer.OBSERVERS,
    "N112": Layer.OBSERVERS,
    # physics
    "N372": Layer.PHYSICS,
    "N373": Layer.PHYSICS,
    "N374": Layer.PHYSICS,
    "N375": Layer.PHYSICS,
    "N376": Layer.PHYSICS,
    "N377": Layer.PHYSICS,
    "N_LeptonMassScale": Layer.PHYSICS,
    "N_WylerStepG": Layer.PHYSICS,
    "N_Bar": Layer.PHYSICS,
    "N240": Layer.PHYSICS,
    "N354": Layer.PHYSICS,
    "N304": Layer.PHYSICS,
    "N000": Layer.PHYSICS,
    "N078": Layer.PHYSICS,  # Gravity as Thermodynamics — Jacobson identity
    "N110": Layer.STRUCTURE,  # Inevitability Theorem for L(3,1)
    "N129": Layer.PHYSICS,  # SM Spectral Triple Algebra derivation
    "N165": Layer.STRUCTURE,  # Ergodicity theorem — Reality Protocol Markov dynamics
    # comms / operations
    "N_CommThm": Layer.COMMS,
    "N_RPfibo": Layer.COMMS,
    "N_RPflow": Layer.COMMS,
    "N_RPsoft": Layer.COMMS,
    "N_MI": Layer.COMMS,
    "N_Shannon": Layer.COMMS,
    "N_Sweller": Layer.COMMS,
    "N_BrownLev": Layer.COMMS,
    "N_SDT": Layer.COMMS,
    "N_SIT": Layer.COMMS,
    "N_LeDoux": Layer.COMMS,
    "N_AestheticEngagement": Layer.COMMS,
    "N048": Layer.COMMS,
    "N001": Layer.COMMS,
    "N336": Layer.COMMS,
    "N330": Layer.COMMS,  # Polarisation as A₀ Binary Compression
    "N332": Layer.COMMS,  # Trust Asymmetry as Second Law in Social Graphs
}


def layer_of(node_id: str) -> Layer:
    return LAYER_MAP.get(node_id, Layer.NUMERIC)
