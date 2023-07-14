import { createContext, useContext, useState } from 'react'

const SelectionContext = createContext();

const SelectionProvider = ({children}) => {
  const [selection, setSelection] =  useState({})

  const value = {
    selection,
    setSelection,
  }

  return <SelectionContext.Provider value={value}>
    {children}
  </SelectionContext.Provider>
}

const useSelectionContext = () => {
  const context = useContext(SelectionContext)

  if (context === undefined)
    throw new Error("useSelectionContext must be used within a SelectionProvider")

  return context
}

export {
  useSelectionContext,
  SelectionProvider
}
