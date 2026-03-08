export function PageHeader({ title, subtitle }: { title: string; subtitle: string }) {
  return (
    <header className="card">
      <h2>{title}</h2>
      <p className="small">{subtitle}</p>
    </header>
  );
}
