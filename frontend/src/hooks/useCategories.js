/**
 * useCategories.js – Loads the category list from /api/categories once.
 */
import { useState, useEffect } from 'react';
import { fetchCategories } from '../services/api';

export function useCategories() {
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError]   = useState(null);

  useEffect(() => {
    let cancelled = false;
    fetchCategories()
      .then(({ categories }) => { if (!cancelled) setCategories(categories); })
      .catch((err)           => { if (!cancelled) setError(err.message); })
      .finally(()            => { if (!cancelled) setLoading(false); });
    return () => { cancelled = true; };
  }, []);

  return { categories, loading, error };
}
