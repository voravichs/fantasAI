import { Link } from "wouter";

export default function Header() {
    return (
        <div className="text-3xl w-full p-5 bg-header">
            <Link href="/">
                <h1 className="text-5xl text-yellow-300 font-bold antialiased flex-center">
                    <span className="font-title">Fantas</span>
                    <span className="font-mono text-6xl tracking-tighter">AI</span>
                </h1>
            </Link>
        </div>
    )
}