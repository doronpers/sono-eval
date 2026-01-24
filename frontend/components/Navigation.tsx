'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';

export function Navigation() {
    const pathname = usePathname();

    const links = [
        { href: '/', label: 'Home' },
        { href: '/assessments', label: 'Assessments' },
        { href: '/analytics', label: 'Analytics' },
        { href: '/batch', label: 'Batch Upload' },
    ];

    return (
        <nav className="border-b border-gray-200 bg-white">
            <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
                <div className="flex h-16 items-center justify-between">
                    <div className="flex items-center">
                        <Link href="/" className="text-xl font-bold text-gray-900">
                            Sono-Eval
                        </Link>
                        <div className="ml-10 flex items-baseline space-x-4">
                            {links.map((link) => (
                                <Link
                                    key={link.href}
                                    href={link.href}
                                    className={`rounded-md px-3 py-2 text-sm font-medium transition-colors ${pathname === link.href
                                            ? 'bg-gray-900 text-white'
                                            : 'text-gray-700 hover:bg-gray-50 hover:text-gray-900'
                                        }`}
                                >
                                    {link.label}
                                </Link>
                            ))}
                        </div>
                    </div>
                    <div className="flex items-center space-x-4">
                        <button className="rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700">
                            New Assessment
                        </button>
                    </div>
                </div>
            </div>
        </nav>
    );
}
