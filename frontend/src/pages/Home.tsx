import Header from "../../components/header";
import Hero from "../../components/hero";
import Footer from "../../components/footer";

export default function Home(){
    return (
    <main className="bg-background min-h-screen">
        <Header />
        <Hero />
        <Footer /> 
    </main>);
}