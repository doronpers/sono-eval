import { type ReactNode } from 'react';
import { clsx } from 'clsx';

interface CardProps {
    children: ReactNode;
    className?: string;
    hover?: boolean;
}

export function Card({ children, className, hover = false }: CardProps) {
    return (
        <div
            className={clsx(
                'rounded-lg border border-gray-200 bg-white p-6 shadow-sm',
                hover && 'transition-shadow hover:shadow-md',
                className
            )}
        >
            {children}
        </div>
    );
}

export function CardHeader({ children, className }: { children: ReactNode; className?: string }) {
    return <div className={clsx('mb-4', className)}>{children}</div>;
}

export function CardTitle({ children }: { children: ReactNode }) {
    return <h3 className="text-lg font-semibold text-gray-900">{children}</h3>;
}

export function CardDescription({ children }: { children: ReactNode }) {
    return <p className="text-sm text-gray-600">{children}</p>;
}

export function CardContent({ children, className }: { children: ReactNode; className?: string }) {
    return <div className={clsx(className)}>{children}</div>;
}
