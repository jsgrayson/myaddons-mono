import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
    title: 'SkillWeaver - WoW Character Optimization',
    description: 'Optimize your World of Warcraft characters with AI-powered recommendations',
}

export default function RootLayout({
    children,
}: {
    children: React.ReactNode
}) {
    return (
        <html lang="en">
            <body className="bg-gray-900 text-white">{children}</body>
        </html>
    )
}
