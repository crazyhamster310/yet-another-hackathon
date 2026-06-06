import { Folder, Home } from "lucide-react";

function App() {
  return (
    <div className="min-h-screen bg-slate-100">
      <aside className="fixed left-0 top-0 h-screen w-16 bg-white border-r border-slate-200">
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
        <h1 className="text-2xl font-semibold text-slate-900">
          Панель управления
        </h1>
      </main>
    </div>
  );
}

export default App;