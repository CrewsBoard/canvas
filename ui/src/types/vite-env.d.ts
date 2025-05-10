interface ImportMeta {
  readonly glob: (path: string) => Record<string, () => Promise<unknown>>;
}
