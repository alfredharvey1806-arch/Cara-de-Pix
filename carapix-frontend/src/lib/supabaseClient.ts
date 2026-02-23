import { createClient } from '@supabase/supabase-js';

const FALLBACK_SUPABASE_URL = 'https://sfqsghgogwtxwzthscvw.supabase.co';
const FALLBACK_SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNmcXNnaGdvZ3d0eHd6dGhzY3Z3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE2NzkzNjAsImV4cCI6MjA4NzI1NTM2MH0.7ntmuAIRC6DKyeZWCKL8KXUiak1x6OH59aVIepAIvDY';

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL || FALLBACK_SUPABASE_URL;
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || FALLBACK_SUPABASE_ANON_KEY;

export const supabase = createClient(supabaseUrl, supabaseAnonKey, {
  auth: { persistSession: false }
});
