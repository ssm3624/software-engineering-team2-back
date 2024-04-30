from supabase import create_client, Client

def get_supabase():
    SUPABASE_URL = 'https://hzjtppomzpnezqwcrhuv.supabase.co'  # 여기에 Supabase 프로젝트 URL 입력
    SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imh6anRwcG9tenBuZXpxd2NyaHV2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTM5OTM0MDUsImV4cCI6MjAyOTU2OTQwNX0.z-0rXCD65TjPakQAoaIb-TVk1PAMI9NRxO2_ndvekbU'
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

    
    return supabase