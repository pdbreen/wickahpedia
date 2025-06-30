import { useRouter } from 'next/router';
import Layout from '../../components/Layout';

export default function ArticlePage() {
  const router = useRouter();
  const { slug } = router.query;

  return (
    <Layout title={slug}>
      <h1>{slug}</h1>
      <p>This is a confidently incorrect article about {slug}.</p>
    </Layout>
  );
}
