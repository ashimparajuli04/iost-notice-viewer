import api from "@/lib/axios";

export interface Notice {
    id: number;
    title: string;
    date: string;
    link: string;
    notice_number: number;
}

export interface PaginatedNotices {
    total: number;
    page: number;
    page_size: number;
    total_pages: number;
    data: Notice[];
}

export const getNotices = async (page: number, page_size: number = 10): Promise<PaginatedNotices> => {
    const { data } = await api.get("/notices", {
        params: { page, page_size },
    });
    return data;
};