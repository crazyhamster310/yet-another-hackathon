import { Folder, Home } from "lucide-react";
import { useEffect, useState } from "react";

function Row(props: any) {
  return (
    <div className="mt-2 flex items-center rounded-2xl bg-white px-6 py-5">
      <div className="w-1/3" style={{ paddingLeft: props.indent }}>
        <span className="font-medium text-slate-900">
          {props.title}
        </span>
      </div>

      <div className="w-1/4 text-sm text-slate-700">
        {props.address}
      </div>

      <div className="w-1/6">
        <span className="rounded-xl bg-slate-100 px-3 py-1 text-sm">
          {props.status}
        </span>
      </div>

      <div className="w-1/6 text-sm text-slate-500">
        {props.id}
      </div>

      <div className="w-32 text-right">
        <button className="rounded-xl border px-4 py-2 text-sm">
          Загрузить
        </button>
      </div>
    </div>
  );
}

function App() {
  const [rows, setRows] = useState<any[]>([]);
  useEffect(() => {
    fetch("http://localhost:8000/api/screens")
      .then((response) => response.json())
      .then((data) => setRows(data))
      .catch((error) => console.log("data load fail:", error));
  }, []);
  return (
    <div className="min-h-screen bg-slate-100">
      <aside className="fixed left-0 top-0 h-screen w-16 border-r border-slate-200 bg-white">
        <div className="mt-6 text-center text-xs font-bold text-slate-900">
          Logo
        </div>

        <nav className="mt-8 flex flex-col items-center gap-5">
          <button className="flex h-10 w-12 items-center justify-center rounded-xl bg-cyan-100 text-cyan-600">
            <Home size={20} strokeWidth={1.8} />
          </button>

          <button className="flex h-10 w-12 items-center justify-center rounded-xl text-slate-500 hover:bg-slate-100">
            <Folder size={21} strokeWidth={1.7} />
          </button>
        </nav>
      </aside>

      <main className="ml-16 p-8">
        <div className="mb-5 flex items-center text-sm text-slate-500">
          <div className="w-1/3">Жилые комплексы</div>
          <div className="w-1/4">Адрес</div>
          <div className="w-1/6">Аптайм</div>
          <div className="w-1/6">ID объекта</div>
          <div className="w-32 text-right">Загрузка</div>
        </div>

        {rows.map((row) => (
          <Row
            key={row.id}
            title={row.title}
            address={row.address}
            status={row.status}
            id={row.id}
            indent={row.indent}
          />
        ))}
      </main>
    </div>
  );
}

export default App;