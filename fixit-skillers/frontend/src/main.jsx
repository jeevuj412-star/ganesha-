import React, { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter, Routes, Route, Link, useNavigate } from "react-router-dom";
import { Wrench, Search, ShieldCheck, CalendarDays, UserRound, LogOut, Menu, X, Star, CheckCircle2 } from "lucide-react";
import api from "./api";
import "./index.css";

function Layout({children}) {
  const navigate = useNavigate();
  const [open,setOpen]=useState(false);
  const user = JSON.parse(localStorage.getItem("fixit_user") || "null");
  const logout=()=>{localStorage.clear();navigate("/");};
  return <div className="min-h-screen">
    <header className="sticky top-0 z-20 bg-white/90 backdrop-blur border-b">
      <div className="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-2 font-black text-xl"><span className="bg-gray-900 text-white p-2 rounded-xl"><Wrench size={20}/></span>Fixit Skillers</Link>
        <nav className="hidden md:flex items-center gap-5 text-sm font-medium">
          <Link to="/services">Services</Link>
          {user && <Link to={user.role==="CUSTOMER"?"/customer":user.role==="WORKER"?"/worker":"/admin"}>Dashboard</Link>}
          {!user ? <><Link to="/login" className="btn-soft">Login</Link><Link to="/register" className="btn-primary">Join Now</Link></> : <button onClick={logout} className="btn-soft flex gap-2"><LogOut size={16}/>Logout</button>}
        </nav>
        <button className="md:hidden" onClick={()=>setOpen(!open)}>{open?<X/>:<Menu/>}</button>
      </div>
      {open && <div className="md:hidden px-4 pb-4 flex flex-col gap-3"><Link to="/services">Services</Link>{user&&<Link to={user.role==="CUSTOMER"?"/customer":user.role==="WORKER"?"/worker":"/admin"}>Dashboard</Link>}{!user&&<Link to="/login">Login</Link>}<button onClick={logout}>Logout</button></div>}
    </header>
    {children}
  </div>
}

function Home(){
 return <Layout><main>
  <section className="bg-gray-950 text-white"><div className="max-w-7xl mx-auto px-4 py-20 grid md:grid-cols-2 gap-12 items-center">
    <div><div className="inline-flex gap-2 bg-white/10 px-3 py-2 rounded-full text-sm"><ShieldCheck size={16}/>Verified local professionals</div>
    <h1 className="text-5xl md:text-6xl font-black mt-5 leading-tight">Every home service.<br/><span className="text-gray-400">One simple platform.</span></h1>
    <p className="text-gray-300 mt-6 text-lg">Find trusted electricians, plumbers, cleaners, carpenters and more near you.</p>
    <div className="flex gap-3 mt-8"><Link to="/services" className="btn bg-white text-gray-950">Book a Service</Link><Link to="/register?role=WORKER" className="btn border border-white/20">Become a Worker</Link></div></div>
    <div className="grid grid-cols-2 gap-4">{["🧹","⚡","🔧","❄️"].map((x,i)=><div key={i} className="h-40 rounded-3xl bg-white/10 border border-white/10 flex items-center justify-center text-6xl">{x}</div>)}</div>
  </div></section>
  <section className="max-w-7xl mx-auto px-4 py-16"><h2 className="text-3xl font-black">How it works</h2><div className="grid md:grid-cols-3 gap-5 mt-8">{[
    ["1","Choose a service","Search for the professional you need."],["2","Book a time","Pick your preferred date, time and address."],["3","Get it done","Track the booking and review the worker."]
  ].map(x=><div className="card p-6" key={x[0]}><div className="w-10 h-10 rounded-xl bg-gray-900 text-white grid place-items-center font-bold">{x[0]}</div><h3 className="font-bold text-lg mt-5">{x[1]}</h3><p className="text-gray-500 mt-2">{x[2]}</p></div>)}</div></section>
 </main></Layout>
}

function Auth({register=false}){
 const nav=useNavigate(); const [role,setRole]=useState(new URLSearchParams(location.search).get("role")||"CUSTOMER");
 const [form,setForm]=useState({name:"",email:"",phone:"",password:"",city:"Bengaluru"});
 const [err,setErr]=useState("");
 const submit=async e=>{e.preventDefault();setErr("");try{const r=await api.post(register?"/auth/register":"/auth/login",register?{...form,role}:{email:form.email,password:form.password});localStorage.setItem("fixit_token",r.data.access_token);localStorage.setItem("fixit_user",JSON.stringify(r.data.user));nav(r.data.user.role==="CUSTOMER"?"/customer":r.data.user.role==="WORKER"?"/worker":"/admin")}catch(e){setErr(e.response?.data?.detail||"Something went wrong")}};
 return <Layout><div className="max-w-md mx-auto px-4 py-14"><div className="card p-7"><h1 className="text-3xl font-black">{register?"Create account":"Welcome back"}</h1><p className="text-gray-500 mt-2">{register?"Join Fixit Skillers":"Sign in to continue"}</p>{register&&<div className="grid grid-cols-2 gap-2 mt-6">{["CUSTOMER","WORKER"].map(r=><button key={r} onClick={()=>setRole(r)} className={role===r?"btn-primary":"btn-soft"}>{r}</button>)}</div>}
 <form onSubmit={submit} className="space-y-4 mt-6">{register&&<input className="input" placeholder="Full name" required value={form.name} onChange={e=>setForm({...form,name:e.target.value})}/>}
 <input className="input" type="email" placeholder="Email" required value={form.email} onChange={e=>setForm({...form,email:e.target.value})}/>
 {register&&<input className="input" placeholder="Phone" value={form.phone} onChange={e=>setForm({...form,phone:e.target.value})}/>}
 <input className="input" type="password" placeholder="Password" required minLength="6" value={form.password} onChange={e=>setForm({...form,password:e.target.value})}/>
 {register&&<input className="input" placeholder="City" value={form.city} onChange={e=>setForm({...form,city:e.target.value})}/>}
 {err&&<div className="bg-red-50 text-red-700 rounded-xl p-3 text-sm">{err}</div>}
 <button className="btn-primary w-full">{register?"Create account":"Login"}</button></form>
 <p className="text-center text-sm text-gray-500 mt-5">{register?<><Link className="underline" to="/login">Already have an account?</Link></>:<Link className="underline" to="/register">Create an account</Link>}</p>
 </div></div></Layout>
}

function Services(){
 const [services,setServices]=useState([]); const [workers,setWorkers]=useState([]); const [selected,setSelected]=useState(null);
 useEffect(()=>{api.get("/services").then(r=>setServices(r.data));api.get("/workers").then(r=>setWorkers(r.data))},[]);
 return <Layout><main className="max-w-7xl mx-auto px-4 py-10"><h1 className="text-4xl font-black">Find a professional</h1><p className="text-gray-500 mt-2">Choose a service and book a verified worker.</p>
 <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mt-8">{services.map(s=><button onClick={()=>{setSelected(s);api.get("/workers",{params:{service_id:s.id}}).then(r=>setWorkers(r.data))}} className={`card p-4 text-left hover:shadow-md ${selected?.id===s.id?"ring-2 ring-gray-900":""}`} key={s.id}><span className="text-3xl">{s.icon}</span><div className="font-bold mt-2">{s.name}</div></button>)}</div>
 <h2 className="text-2xl font-black mt-12">{selected?selected.name:"Available professionals"}</h2>
 <div className="grid md:grid-cols-3 gap-5 mt-5">{workers.map(w=><div className="card p-5" key={w.id}><div className="flex justify-between"><div><h3 className="font-bold text-lg">{w.name}</h3><p className="text-sm text-gray-500">{w.service} · {w.city}</p></div>{w.verified&&<ShieldCheck className="text-green-600"/>}</div><div className="flex gap-3 text-sm mt-4"><span><Star size={15} className="inline fill-current"/> {w.rating.toFixed(1)}</span><span>{w.experience_years} yrs</span><span>{w.completed_jobs} jobs</span></div><p className="text-gray-600 text-sm mt-4">{w.bio||"Skilled local professional."}</p><Link to={`/book/${w.id}`} className="btn-primary block text-center mt-5">Book Now</Link></div>)}</div>
 </main></Layout>
}

function Customer(){
 const [bookings,setBookings]=useState([]); const [msg,setMsg]=useState("");
 const load=()=>api.get("/bookings/mine").then(r=>setBookings(r.data)); useEffect(load,[]);
 return <Layout><main className="max-w-6xl mx-auto px-4 py-10"><h1 className="text-4xl font-black">Customer Dashboard</h1><p className="text-gray-500">Your bookings and service activity.</p><Link to="/services" className="btn-primary inline-block mt-6">Find a Service</Link><div className="grid md:grid-cols-2 gap-4 mt-8">{bookings.map(b=><div className="card p-5" key={b.id}><div className="flex justify-between"><b>Booking #{b.id}</b><span className="px-2 py-1 rounded-lg bg-gray-100 text-xs">{b.status}</span></div><p className="text-gray-500 mt-3">{new Date(b.scheduled_at).toLocaleString()}</p><p className="mt-2">{b.address}</p>{["PENDING","ACCEPTED","IN_PROGRESS"].includes(b.status)&&<button onClick={()=>api.post(`/bookings/${b.id}/cancel`).then(()=>{setMsg("Cancelled");load()})} className="btn-soft mt-4">Cancel</button>}</div>)}</div>{msg&&<p className="mt-4 text-green-700">{msg}</p>}</main></Layout>
}

function Book({id}){
 const nav=useNavigate(); const [w,setW]=useState(null); const [services,setServices]=useState([]); const [f,setF]=useState({service_id:"",address:"",scheduled_at:"",description:"",budget:0}); const [err,setErr]=useState("");
 useEffect(()=>{api.get("/workers").then(r=>setW(r.data.find(x=>x.id==id)));api.get("/services").then(r=>setServices(r.data))},[id]);
 const submit=async e=>{e.preventDefault();try{await api.post("/bookings",{...f,worker_id:Number(id),service_id:Number(f.service_id),budget:Number(f.budget)});nav("/customer")}catch(e){setErr(e.response?.data?.detail||"Booking failed")}};
 if(!w)return <Layout><div className="p-10 text-center">Loading...</div></Layout>;
 return <Layout><div className="max-w-xl mx-auto px-4 py-10"><div className="card p-7"><h1 className="text-3xl font-black">Book {w.name}</h1><p className="text-gray-500">{w.service} · ⭐ {w.rating.toFixed(1)}</p><form onSubmit={submit} className="space-y-4 mt-6"><select className="input" required value={f.service_id} onChange={e=>setF({...f,service_id:e.target.value})}><option value="">Select service</option>{services.map(s=><option key={s.id} value={s.id}>{s.name}</option>)}</select><input className="input" type="datetime-local" required value={f.scheduled_at} onChange={e=>setF({...f,scheduled_at:e.target.value})}/><textarea className="input" placeholder="Service address" required value={f.address} onChange={e=>setF({...f,address:e.target.value})}/><textarea className="input" placeholder="Describe the work" value={f.description} onChange={e=>setF({...f,description:e.target.value})}/><input className="input" type="number" placeholder="Budget (₹)" value={f.budget} onChange={e=>setF({...f,budget:e.target.value})}/>{err&&<p className="text-red-600">{err}</p>}<button className="btn-primary w-full">Confirm Booking</button></form></div></div></Layout>
}

function Worker(){
 const [me,setMe]=useState(null);const [bookings,setBookings]=useState([]);const [kyc,setKyc]=useState(null);const [form,setForm]=useState({legal_name:"",dob:"",address:"",aadhaar_last4:"",pan_masked:""});const [msg,setMsg]=useState("");
 const load=()=>{api.get("/workers/me").then(r=>setMe(r.data));api.get("/bookings/worker").then(r=>setBookings(r.data));api.get("/workers/kyc").then(r=>{setKyc(r.data);if(r.data)setForm({legal_name:r.data.legal_name||"",dob:r.data.dob||"",address:r.data.address||"",aadhaar_last4:r.data.aadhaar_last4||"",pan_masked:r.data.pan_masked||""})})};useEffect(load,[]);
 const act=(id,a)=>api.post(`/bookings/${id}/${a}`).then(load);
 const submit=e=>{e.preventDefault();api.post("/workers/kyc",form).then(r=>{setMsg(r.data.message);load()}).catch(e=>setMsg(e.response?.data?.detail||"KYC failed"))};
 return <Layout><main className="max-w-6xl mx-auto px-4 py-10"><div className="flex justify-between items-start"><div><h1 className="text-4xl font-black">Worker Dashboard</h1><p className="text-gray-500">{me?.name} · {me?.service}</p></div>{me?.verified&&<span className="bg-green-50 text-green-700 px-3 py-2 rounded-xl flex gap-2"><ShieldCheck size={18}/>Verified</span>}</div>
 <div className="grid md:grid-cols-3 gap-4 mt-8"><div className="card p-5"><b>Rating</b><div className="text-3xl font-black mt-2">⭐ {me?.rating?.toFixed(1)}</div></div><div className="card p-5"><b>Completed jobs</b><div className="text-3xl font-black mt-2">{me?.completed_jobs}</div></div><div className="card p-5"><b>Availability</b><button onClick={()=>api.post(`/workers/availability?available=${!me?.available}`).then(load)} className="btn-soft mt-2 block">{me?.available?"Available":"Unavailable"}</button></div></div>
 <div className="grid lg:grid-cols-2 gap-6 mt-8"><section><h2 className="text-2xl font-black">Booking requests</h2><div className="space-y-3 mt-4">{bookings.map(b=><div className="card p-5" key={b.id}><div className="flex justify-between"><b>#{b.id}</b><span>{b.status}</span></div><p className="text-gray-500 mt-2">{new Date(b.scheduled_at).toLocaleString()}</p><p>{b.address}</p><div className="flex flex-wrap gap-2 mt-4">{b.status==="PENDING"&&<><button className="btn-primary" onClick={()=>act(b.id,"accept")}>Accept</button><button className="btn-soft" onClick={()=>act(b.id,"reject")}>Reject</button></>}{b.status==="ACCEPTED"&&<button className="btn-primary" onClick={()=>act(b.id,"start")}>Start Job</button>}{b.status==="IN_PROGRESS"&&<button className="btn-primary" onClick={()=>act(b.id,"complete")}>Complete Job</button>}</div></div>)}</div></section>
 <section><h2 className="text-2xl font-black">KYC verification</h2><div className="card p-5 mt-4"><p className="text-sm text-gray-500">Status: <b>{kyc?.status||"NOT SUBMITTED"}</b></p><form onSubmit={submit} className="space-y-3 mt-4"><input className="input" placeholder="Legal name" required value={form.legal_name} onChange={e=>setForm({...form,legal_name:e.target.value})}/><input className="input" placeholder="Date of birth" value={form.dob} onChange={e=>setForm({...form,dob:e.target.value})}/><textarea className="input" placeholder="Full address" required value={form.address} onChange={e=>setForm({...form,address:e.target.value})}/><input className="input" placeholder="Aadhaar last 4 digits" maxLength="4" value={form.aadhaar_last4} onChange={e=>setForm({...form,aadhaar_last4:e.target.value.replace(/\\D/g,"")})}/><input className="input" placeholder="Masked PAN e.g. ABCDE****F" value={form.pan_masked} onChange={e=>setForm({...form,pan_masked:e.target.value})}/><p className="text-xs text-gray-500">For this MVP, document uploads are not stored. Production should use secure encrypted object storage.</p><button className="btn-primary">Submit KYC</button>{msg&&<p className="text-green-700">{msg}</p>}</form></div></section></div>
 </main></Layout>
}

function Admin(){
 const [stats,setStats]=useState({});const [kyc,setKyc]=useState([]);
 const load=()=>{api.get("/admin/stats").then(r=>setStats(r.data));api.get("/workers/admin/kyc").then(r=>setKyc(r.data))};useEffect(load,[]);
 const decision=(id,status)=>api.post(`/workers/admin/kyc/${id}/decision?status=${status}`).then(load);
 return <Layout><main className="max-w-7xl mx-auto px-4 py-10"><h1 className="text-4xl font-black">Admin Dashboard</h1><div className="grid grid-cols-2 md:grid-cols-6 gap-3 mt-8">{Object.entries(stats).map(([k,v])=><div className="card p-4" key={k}><div className="text-xs uppercase text-gray-500">{k.replace("_"," ")}</div><div className="text-2xl font-black mt-2">{v}</div></div>)}</div><h2 className="text-2xl font-black mt-10">KYC Reviews</h2><div className="space-y-3 mt-4">{kyc.length===0?<div className="card p-5 text-gray-500">No KYC submissions.</div>:kyc.map(k=><div className="card p-5" key={k.id}><div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4"><div><b>{k.worker_name}</b><p className="text-sm text-gray-500">{k.legal_name} · Aadhaar ****{k.aadhaar_last4||"----"} · {k.status}</p><p className="text-sm mt-1">{k.address}</p></div>{k.status==="PENDING"&&<div className="flex gap-2"><button className="btn-primary" onClick={()=>decision(k.id,"VERIFIED")}>Approve</button><button className="btn-soft" onClick={()=>decision(k.id,"REJECTED")}>Reject</button></div>}</div></div>)}</div></main></Layout>
}

function App(){
 return <Routes><Route path="/" element={<Home/>}/><Route path="/login" element={<Auth/>}/><Route path="/register" element={<Auth register/>}/><Route path="/services" element={<Services/>}/><Route path="/customer" element={<Customer/>}/><Route path="/worker" element={<Worker/>}/><Route path="/admin" element={<Admin/>}/><Route path="/book/:id" element={<Book id={location.pathname.split("/").pop()}/>}/></Routes>
}

createRoot(document.getElementById("root")).render(<BrowserRouter><App/></BrowserRouter>);
