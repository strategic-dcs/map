import { SelectionProvider } from './contexts/SelectionContext';
import { ThemeProvider, createTheme } from '@mui/material';
import { AxiosInstanceProvider } from './contexts/AxiosContext.jsx';
import { Navigate, Route, Routes } from 'react-router-dom';
import TopBar from './components/TopBar/TopBar.jsx';
import Map from './pages/map/Map.jsx';
import StatsRouter from './pages/stats/StatsRouter';

const darkTheme = createTheme({
  palette: {
    mode: 'dark',
  },
  typography: {
    fontFamily: "Montserrat"
  }
});

function App() {
  return (
    <ThemeProvider theme={darkTheme}>
      <AxiosInstanceProvider>
        <SelectionProvider>
          <TopBar />
          <Routes>
            <Route path="/stats/*" element={<StatsRouter/>} />
            <Route path="/map/*" element={<Map />} />
            <Route path="" element={<Navigate to="/map" replace />} />
          </Routes>
        </SelectionProvider>
      </AxiosInstanceProvider>
    </ThemeProvider>
  )
}

export default App;
