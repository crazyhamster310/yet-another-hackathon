import { useEffect, useState } from "react";
import DisplayPlayer from "./components/DisplayPlayer";
import AdminPanel from "./components/AdminPanel";
import TemplatesPanel from "./components/TemplatesPanel";

export default function App() {
  const [currentPath, setCurrentPath] = useState(window.location.pathname);

  useEffect(() => {
    const onLocationChange = () => setCurrentPath(window.location.pathname);
    window.addEventListener("popstate", onLocationChange);

    const originalPushState = window.history.pushState;
    window.history.pushState = function (...args) {
      originalPushState.apply(this, args);
      onLocationChange();
    };
    return () => window.removeEventListener("popstate", onLocationChange);
  }, []);

  const navigate = (path: string) => {
    window.history.pushState({}, "", path);
  };

  if (currentPath.startsWith("/player/")) {
    return <DisplayPlayer slug={currentPath.split("/")[2]} />;
  }

  if (currentPath === "/templates") {
    return <TemplatesPanel onNavigate={navigate} />;
  }

  return <AdminPanel onNavigate={navigate} />;
}
