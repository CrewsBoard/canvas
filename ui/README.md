# CrewsBoard Canvas UI

This is the frontend application for CrewsBoard Canvas, a visual workflow
builder for AI agents and crews.

## Project Structure

```
src/
├── components/           # Reusable UI components
│   ├── sidebar/         # Sidebar related components
│   │   ├── Sidebar.tsx              # Main sidebar component
│   │   └── sidebarProps.types.ts    # Sidebar prop types
│   │
│   └── shared/          # Shared UI components
│
├── flow-nodes/          # Flow node implementations
│   ├── crewai-crew-node/    # CrewAI crew node
│   │   └── CrewaiCrewNode.tsx      # Crew node component
│   │
│   ├── crewai-agent-node/   # CrewAI agent node
│   ├── output-node/         # Output node
│   ├── transform-node/      # Transform node
│   └── input-node/          # Input node
│
├── libs/                # Core libraries and utilities
│   ├── providers/       # Context providers
│   │   ├── BootstrapperProvider.tsx  # Application bootstrapping
│   │   └── QueryProvider.tsx         # Query context provider
│   │
│   ├── services/        # Service layer implementations
│   │   └── uiComponentLoaderService.ts  # UI component loading service
│   │
│   ├── http/            # HTTP client and related utilities
│   │   ├── http.ts          # HTTP utilities
│   │   └── httpClient.ts    # HTTP client implementation
│   │
│   └── hooks/           # Custom React hooks
│       └── useHttpClient.ts  # HTTP client hook
│
├── modules/             # Feature modules
│   ├── root/            # Root module
│   │   ├── RootModule.tsx    # Root module component
│   │   └── services/         # Root module services
│   │
│   └── shared/          # Shared module components
│       └── example/          # Example module
│
├── pages/               # Page components
│   └── RootPage.tsx     # Root page component
│
├── stores/              # State management
│   └── nodeRegistryStore.ts  # Node registry store
│
├── types/               # TypeScript type definitions
│   ├── http.types.ts    # HTTP related types
│   ├── stores.types.ts  # Store related types
│   ├── flowNode.types.ts # Flow node types
│   └── providers.types.ts # Provider types
│
├── App.tsx              # Main application component
├── Routes.tsx           # Application routes
├── main.tsx             # Application entry point
└── index.css            # Global styles
```

## Key Features

- Visual workflow builder for AI agents and crews
- Modular node-based architecture
- Type-safe implementation with TypeScript
- State management with stores
- Reusable component library
- HTTP service layer for API communication
- Custom hooks for shared logic

## Development

The project follows a modular architecture with clear separation of concerns:

- `components/`: Reusable UI components
- `flow-nodes/`: Individual node implementations
- `libs/`: Core utilities and services
- `modules/`: Feature-specific modules
- `stores/`: State management
- `types/`: TypeScript type definitions
