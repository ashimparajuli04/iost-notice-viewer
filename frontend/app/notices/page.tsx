"use client";
import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { getNotices } from "@/lib/api/notices";

export default function NoticesPage() {
    const [page, setPage] = useState(1);

    const { data, isLoading, isError } = useQuery({
        queryKey: ["notices", page],       // refetches automatically when page changes
        queryFn: () => getNotices(page),
    });

    if (isLoading) return <p>Loading...</p>;
    if (isError) return <p>Failed to load notices.</p>;

    return (
        <div>
            {data?.data.map((notice) => (
                <div key={notice.id}>
                    <p>{notice.title}</p>
                    <p>{notice.date}</p>
                </div>
            ))}

            {/* Pagination controls */}
            <div>
                <button
                    onClick={() => setPage((p) => p - 1)}
                    disabled={page === 1}
                >
                    Previous
                </button>
                <span> Page {page} of {data?.total_pages} </span>
                <button
                    onClick={() => setPage((p) => p + 1)}
                    disabled={page === data?.total_pages}
                >
                    Next
                </button>
            </div>
        </div>
    );
}